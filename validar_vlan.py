vlan = int(input("Ingresa el número de VLAN: "))

if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} es del rango normal (1-1005).")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} es del rango extendido (1006-4094).")
else:
    print(f"La VLAN {vlan} está fuera del rango permitido (1-4094).")
