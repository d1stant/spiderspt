from base64 import b64decode, b64encode
from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
from typing import Literal

from Crypto.Cipher import AES
from Crypto.Cipher._mode_cbc import CbcMode
from Crypto.Cipher._mode_gcm import GcmMode
from Crypto.Cipher.AES import MODE_CBC, MODE_GCM
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util.Padding import pad

from spiderspt._type_ import Base64Str


def md5_encrypt(plaintext: str, return_: Literal["upper", "lower"] = "upper") -> str:
    """MD5加密

    Args:
        text (str): 要加密的明文
        return_ (Literal["upper", "lower"], optional): 返回模式[大写, 小写]. Defaults to "upper".

    Returns:
        str: 加密后的32位字符串
    """
    ciphertext: str = md5(plaintext.encode("utf-8")).hexdigest()
    if return_ == "upper":
        return ciphertext.upper()
    return ciphertext


@dataclass
class AesEncryptedResult:
    """AES加密结果对象"""

    mode: str
    ciphertext: Base64Str
    iv: Base64Str | None = None
    nonce: Base64Str | None = None
    tag: Base64Str | None = None
    associated_data: Base64Str | None = None


def aes_cbc_encrypt(plaintext: str, key: bytes) -> AesEncryptedResult:
    """AES CBC加密

    Args:
        plaintext (str): 明文
        key (bytes): 密钥

    Returns:
        dict[str, Base64String]: {"iv": IV, "ciphertext": 密文}
    """
    iv: bytes = get_random_bytes(16)
    cipher: CbcMode = AES.new(key, MODE_CBC, iv)
    padded_data: bytes = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext: bytes = cipher.encrypt(padded_data)
    return AesEncryptedResult(
        mode="CBC",
        iv=b64encode(iv).decode("utf-8"),
        ciphertext=b64encode(ciphertext).decode("utf-8"),
    )


def aes_gcm_encrypt(
    plaintext: str, key: bytes, associated_data: bytes | None = None
) -> AesEncryptedResult:
    """AES GCM加密

    Args:
        plaintext (str): 明文
        key (bytes): 密钥
        associated_data (bytes | None, optional): 关联数据. Defaults to None.

    Returns:
        dict[str, Base64String]: {"nonce": nonce, "ciphertext": 密文, "tag": 认证标签, "associated_data": 关联数据}
    """
    cipher: GcmMode = AES.new(key, MODE_GCM)
    if associated_data:
        cipher.update(associated_data)
    digest: tuple[bytes, bytes] = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    ciphertext: bytes = digest[0]
    tag: bytes = digest[1]
    return AesEncryptedResult(
        mode="GCM",
        nonce=b64encode(cipher.nonce).decode("utf-8"),
        ciphertext=b64encode(ciphertext).decode("utf-8"),
        tag=b64encode(tag).decode("utf-8"),
        associated_data=b64encode(associated_data).decode("utf-8")
        if associated_data
        else "",
    )


RSA_KEY_PATH = Path("./RSA_KEY")
RSA_KEY_PATH.mkdir(parents=True, exist_ok=True)
RSA_PRIVATE_KEY: Path = RSA_KEY_PATH / "private.pem"
RSA_PUBLIC_KEY: Path = RSA_KEY_PATH / "public.pem"
RSA_DEFAULT_PRIVATE_KEY: RsaKey = RSA.import_key("""-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAsam6FF/ZuMDIE/Hv9SJru7F2sZFe8PQVgnZPPYfw0vf/ZABu
Xc0qqrI7bGJY9biE8OnwixmWHSXWEzcIlk8Bz6qB+9cX3BjWKjP9Jal8mBsI6i6m
E/ALRz4uwdMN9LXWs4l7OgvMsTuNgjmgVvHFEdOsrYhN7auqicXddq8g/kMmdUdQ
vZygVQD3ukA7Dr4Va2ZFit6/QXNy0lG8cfwacY6pmU54h3crEdEr/elGfKway1Bp
J1Ay7qNlNQ4PjOQ0Kx3U/bo2EZRm4QjNopW7L9Rlh3ysKIh9B3EUsvS2vVRetLUG
D2+EKuWERi59643EUmAmBy6Nqx43jNnEumCVjwIDAQABAoIBAFbqkAxzsBJAziFj
1V75zfbvJQBN/EKpRvSiaLXTka/Ef/8ubtAZFWyY8ZVer+LWuMMb0ABdLiFoZ0jT
PbI7SMmNwzWvzw5wYCYZdRk9x6SqZTwcQkeywfHCrCFK3aMAat8+vThymVuDpQE2
rAidEypbgjkLXASQXUg1stjjaKK66Ggl9xnwspFnojtugezKMSMN6nloCs5vs1or
MN2mvV1AqLe0/xQIISgUGtHRn7KZDS6tu5F04SmJPHAfXSAju//bRGAlHkytaS89
yhe1vEb+4husgNsQh4/oGkeO4+/xhS33b5jJly5pqGTCZccDGaqFj6G8Rdo1MIIZ
fKVEd8ECgYEAuEC7+oftpnq203UvflVb/o8lt+qI6arQrMXoofdiTTWtD+JfWxnk
4vQpL+abJBM0/OwJ01BSHXQinfRwng2XgKbPy0D2AMvZgRucfyfo2DP4b45yfsI7
0UKLLt024LpGWFeVoaKcxGi5LjpZ3WUtiEM21FGaegQJzKlheqRCR/ECgYEA9tgU
mMkUXAeXnEjkXURH9umLxXGOy1UcWQdcKQUem7bDUsbv9H248wPbKIysnHpKa8mR
A9+EM/35HxJGPghvXnPxQYWhGsPvlKCPB1M3mBEvQzoHaRRV0PUkq7G86e9GAN/f
U/F3/0R1QqgMsKyhepCtOO5RN7T7AUp0Urg6NX8CgYAFflicdaUOS6Zb06ig2aau
hlIXk7SVUvR50kTHX3rc1nbcfGFfc/wxEBqSRQvnHXN8/wSj+kcYfbfygbFB5SHZ
Qh/77WnoSCup/8rAt83ndFU57kNXqC7kZFmGAi56sNMcGzBo61JFQOIUkMTRJw0e
fPKLjgtPDAPGyF4RrAgV4QKBgDCzXQzvzyaBEPZyoyuLhy890Ke5ydRwDFG8VAB7
1BggrNSuDzWLgGvhvOF5L60Hq5ssf4HmHW0slHP+5QDkJSTbdyPYO3rOYXxPWSi2
0GceLNb0ofWnX28EjqGZRY5Z+NO/V452O5iPZxspkKdix9EoriRnUHrPKB6PE/gm
BMX9AoGADTiX23rOnltUhDchGSWvGp4Y7TVAq6Bb0Lo0oNOg/cP8nQPkKTopf8FS
rsPRFMBNfTuJglY4lbu/lXE1pnd4TfFo7crEqKKC4x6AupfmXnXgt2AD3MKeO/93
oUCJNrdUs/vjTL/q8nSzTb1T7+rFofwqEtnnJsBpvO8d87qOCzw=
-----END RSA PRIVATE KEY-----""")
RSA_DEFAULT_PUBLIC_KEY: RsaKey = RSA.import_key("""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsam6FF/ZuMDIE/Hv9SJr
u7F2sZFe8PQVgnZPPYfw0vf/ZABuXc0qqrI7bGJY9biE8OnwixmWHSXWEzcIlk8B
z6qB+9cX3BjWKjP9Jal8mBsI6i6mE/ALRz4uwdMN9LXWs4l7OgvMsTuNgjmgVvHF
EdOsrYhN7auqicXddq8g/kMmdUdQvZygVQD3ukA7Dr4Va2ZFit6/QXNy0lG8cfwa
cY6pmU54h3crEdEr/elGfKway1BpJ1Ay7qNlNQ4PjOQ0Kx3U/bo2EZRm4QjNopW7
L9Rlh3ysKIh9B3EUsvS2vVRetLUGD2+EKuWERi59643EUmAmBy6Nqx43jNnEumCV
jwIDAQAB
-----END PUBLIC KEY-----""")


@dataclass
class RsaKeyPair:
    """RSA密钥对"""

    private: str
    public: str


@dataclass
class RsaSignatureResult:
    """RSA加密结果对象"""

    msg: str
    signature: Base64Str


def generate_rsa_key(save: bool = True) -> RsaKeyPair:
    """生成RSA密钥对

    Args:
        save (bool, optional): 是否保存到本地文件. Defaults to True.

    Returns:
        RsaKeyPair: 密钥对
    """
    key: RsaKey = RSA.generate(2048)
    private_key: bytes = key.exportKey()
    public_key: bytes = key.publickey().exportKey()
    if save:
        RSA_PRIVATE_KEY.write_bytes(private_key)
        RSA_PUBLIC_KEY.write_bytes(public_key)
    return RsaKeyPair(
        private=private_key.decode("utf-8"), public=public_key.decode("utf-8")
    )


def rsa_signature(
    msg: Base64Str, private_key: RsaKey = RSA_DEFAULT_PRIVATE_KEY
) -> RsaSignatureResult:
    """RSA私钥对数据签名

    Args:
        msg (str): 要签名的内容
        private_key (RsaKey, optional): 私钥. Defaults to RSA_DEFAULT_PRIVATE_KEY.

    Returns:
        RsaEncryptedResult: _description_
    """
    signature: bytes = PKCS1_v1_5.new(private_key).sign(SHA256.new(msg.encode("utf-8")))
    return RsaSignatureResult(msg, b64encode(signature).decode("utf-8"))


def rsa_verify(
    signature_result: RsaSignatureResult, public_key: RsaKey = RSA_DEFAULT_PUBLIC_KEY
) -> bool:
    try:
        PKCS1_v1_5.new(public_key).verify(  # pylint: disable=not-callable
            SHA256.new(signature_result.msg.encode("utf-8")),
            b64decode(signature_result.signature),
        )
    except (ValueError, TypeError):
        return False
    return True
