import json
import pprint

import flask
from flask import Blueprint, render_template, url_for, current_app, session

runes_blueprint = Blueprint("rune", __name__)

die_size_map = {4: "1d6", 6: "1d8", 8: "2d4", 10: "1d12", 12: "2d6"}
format = ["#name#", "#damageStat#", "#dtype#", "#flavorText#", "#criton#", "#attackBonus#", "#upDie1#", "#upDie2#",
          "#downDie1#", "#damageMod#", "#dmgDie#", "#runeVal#"]


@runes_blueprint.route('/')
def runes():
    f = open('json/rune.json', encoding="utf8")
    runes = json.load(f)

    runes = sorted(runes, key=lambda r: r["name"])

    return render_template('/runes/runes.html', runes=runes)


@runes_blueprint.route('/build_weapon', methods=['POST'])
def weapon():
    form = flask.request.form.to_dict()

    weapon = buildWeapon(form)

    return json.dumps(weapon)


def buildWeapon(form):
    out = []

    attackMod = 'max(dexterityMod,strengthMod)' if form.get('weapon-type-finesse') else 'strengthMod' if form.get(
        'weapon-type') == "melee" else 'dexterityMod'
    damage = {"type": "damage", "damage": f"{form.get('damage-die')}+{{{attackMod}}} [{form.get('damage-type')}]"}
    attack = {"type": "attack", "attackBonus": f"proficiencyBonus+{attackMod}", "hit": [damage], "miss": []}
    target = {"type": "target", "target": "all", "effects": [attack]}
    base = {"name": form.get('weapon-name'), "_v": 2, "automation": [target], "criton": form.get('crit-range')}

    if form.get('weapon-text'):
        text = {"type": "text", "text": form.get('weapon-text'), "title": "Effect"}
        base['automation'].append(text)

    if form.get('weapon-type-versatile'):
        die = form.get('damage-die')
        size = int(die[die.find("d")+1:])
        try:
            new = json.dumps(base).replace(die, die_size_map[size]).replace(form.get('weapon-name'), f'2-Handed {form.get("weapon-name")}')
            out.append(json.loads(new))
        except:
            pass

    out.append(base)

    weapons = processRunes(out, form)

    return weapons

def getRunes(form):
    f = open('json/rune.json', encoding="utf8")
    runes = json.load(f)
    out = []

    for rune in runes:
        if form.get(rune.get('name')):
            out.append(rune)

def processRunes(attacks, form):
    f = open('json/rune.json', encoding="utf8")
    runes = json.load(f)
    flavorText = form.get('weapon-text')
    out = []

    for attack in attacks:
        name = attack.get("name")
        a = json.dumps(attack)
        test = getUpDie(a, 1)
        for rune in runes:
            val = get_rune_value(rune, form)
            if form.get(rune.get('name')):
                match rune.get('type'):
                    case "flavor":
                        pass
                    case "hit_bonus":
                        # val = get_rune_value(rune, form)
                        a = a.replace('attackBonus": "', f'attackBonus": "{val}+')

                    case "dmg_bonus":
                        # val = get_rune_value(rune, form)
                        a = a.replace('} [', '}' + f'+{val} [')

                    case "stat":
                        # val = get_rune_value(rune, form)
                        bonus = get_attack_bonus(a)
                        if val in bonus:
                            pass
                        elif "dexterityMod" in bonus:
                            a = a.replace('dexterityMod', val)
                        elif "strengthMod" in bonus:
                            a = a.replace('strengthMod', val)

                    case "hit_effect":
                        if save := rune.get("save"):
                            dc = 12 + int(get_rune_value(rune, form))
                            s = {"type": "save", "stat": save.get("type"), "fail": [], "success": [], "dc": dc}
                            if fail := save.get("fail"):
                                if damage := fail.get("damage"):
                                    dmg = {"type": "damage", "damage": damage}
                                    s["fail"].append(dmg)

                                if effect := fail.get("effect"):
                                    e = {"type": "ieffect2", "name": effect.get("name"),
                                         "duration": effect.get("duration", -1),
                                         "effects": effect.get("effects"),
                                         "end": effect.get("end", False),
                                         "conc": effect.get("conc", False),
                                         "desc": effect.get("desc", ""),
                                         "tick_on_caster": effect.get("tick_on_caster", False)}
                                    s["fail"].append(e)

                            if success := save.get("success"):
                                if damage := success.get("damage"):
                                    dmg = {"type": "damage", "damage": damage}
                                    s["success"].append(dmg)

                                if effect := success.get("effect"):
                                    e = {"type": "ieffect2", "name": effect.get("name"),
                                         "duration": effect.get("duration", -1),
                                         "effects": effect.get("effects"),
                                         "end": effect.get("end", False),
                                         "conc": effect.get("conc", False),
                                         "desc": effect.get("desc", ""),
                                         "tick_on_caster": effect.get("tick_on_caster", False)}
                                    s["success"].append(dmg)

                        a = append_on_hit(a,s)

                    case "attack":
                        damageStat = get_attack_stat(a)
                        attackBonus = get_attack_bonus(a)
                        damageMod = get_damage_bonus(a)
                        dtype = get_damage_type(a)
                        criton = int(get_criton(a))
                        on_hit = get_on_hit_effects(a)
                        upDie1 = getUpDie(a)
                        upDie2 = getUpDie(a, 1)
                        downDie1 = getUpDie(a, -1)
                        dmgDie = get_damage_die(a)

                        r = [name, damageStat, dtype, flavorText, criton, attackBonus, upDie1, upDie2, downDie1, damageMod, dmgDie, val]
                        if new_atk := rune.get("attack"):
                            for i in range(len(format)):
                                new_atk = new_atk.replace(format[i], str(r[i]))

                            for eff in on_hit:
                                new_atk = append_on_hit(new_atk, eff)

                            if rune.get("replace"):
                                a = new_atk
                            else:
                                out.append(json.loads(new_atk))

        out.append(json.loads(a))

    return out

def get_rune_value(rune, form):
    if rune.get('value'):
        return rune.get('value').replace('#upgrade#', form.get(f'{rune.get("name")}-upgrade',""))

    return None

def get_attack_stat(a):
    bonus = get_attack_bonus(a)
    return "max(dexterityMod,strengthMod)" if "max" in bonus else "dexterityMod" if "dex" in bonus else "strengthMod"
def get_attack_bonus(a):
    index = a.find('"attackBonus": "') + 16
    return str(a[index:a[index:].find('"') + index])

def get_damage_bonus(a):
    index = a.find('}+')+1
    if index:
        return str(a[index:a[index:].find(" [") + index])
    return ""

def get_damage_type(a):
    attack_str = get_attack_str(a)

    return str(attack_str[attack_str.find('[') + 1:attack_str.find(']')])

def get_attack_str(a):
    dindex = a.find('"damage": "') + 11

    attack_str = str(a[dindex:a[dindex:].find('"') + dindex])
    return attack_str

def get_criton(a):
    index = a.find('"criton": ') + 11
    crit = str(a[index:a[index:].find('}')-1 + index])
    return crit

def get_damage_die(a):
    dindex = a.find('"damage": "') + 11
    damage_str = str(a[dindex:a[dindex:].find('+') + dindex])
    return damage_str

def append_on_hit(a, automation):
    atk = json.loads(a)
    for effect in atk["automation"]:
        if 'effects' in effect:
            for effect_type in effect['effects']:
                if 'hit' in effect_type:
                    effect_type['hit'].append(automation)
                    break

    return json.dumps(atk)

def getUpDie(a, add_steps=0):
    attackDie = get_damage_die(a)
    size = int(attackDie[attackDie.find("d") + 1:])
    tmp = list(die_size_map.items())
    idx = [i for i, k in enumerate(tmp) if k[0] == size][0]+add_steps

    if attackDie == "2d6" or idx > len(die_size_map)-1:
        return "2d6"

    return list(die_size_map.values())[idx]

def get_on_hit_effects(a):
    atk = json.loads(a)
    eff = None

    for effect in atk["automation"]:
        if "target" in effect:
            for effect_type in effect["effects"]:
                if "hit" in effect_type:
                    eff = [e for e in effect_type['hit'] if e["type"] != "damage"]
                    break

    return eff



