import huobi

keys = open('keys.txt', 'r').readlines()
private_key = keys[0].strip()
public_key = keys[1].strip()

huobi = huobi.Huobi(private_key, public_key)
# huobi.request('test', {'a': 'a'})