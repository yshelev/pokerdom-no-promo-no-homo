import secrets
from sympy import isprime
from math import gcd


def generate_large_prime(bits: int = 1024) -> int:
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1  
        if isprime(candidate):
            return candidate

def generate_key(p: int) -> int:
    phi = p - 1
    while True:
        k = secrets.randbelow(phi - 2) + 2  
        if gcd(k, phi) == 1:
            return k, p