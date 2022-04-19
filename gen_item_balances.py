#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2020 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import sys
import csv
from bl3hotfixmod.bl3hotfixmod import Balance

# Data generated by this script lives online at:
# https://docs.google.com/spreadsheets/d/1XYG30B6CulmcmmVDuq-PkLEJVtjAFacx7cuSkqbv5N4/edit?usp=sharing
from hotfixgenerator.bl3data import BL3Data

data = BL3Data()

# Balances to loop through
gun_balances = []

# Some text massaging
transforms = {
        'sniperrifles': 'Sniper Rifles',
        'sniperifles': 'Sniper Rifles',
        'assaultrifles': 'ARs',
        'assaultrifle': 'ARs',
        'shotgun': 'Shotguns',
        'pistol': 'Pistols',
        'heavyweapons': 'Heavy Weapons',
        'hw': 'Heavy Weapons',

        '_etech': 'E-Tech',

        'childrenofthevault': 'COV',
        'ted': 'Tediore',
        'vla': 'Vladof',
        'tor': 'Torgue',
        'atl': 'Atlas',
        'mal': 'Maliwan',
        }

# "Regular" guns - second glob just matches on etech
for glob_pattern, re_pattern in [
        ('\\Game\\Gear\\Weapons\\*\\*\\*Shared\\_Design\\*Balance*\\Balance_*',
         r'^\\Game\\Gear\\Weapons\\(?P<guntype>.*?)\\(?P<manufacturer>.*?)\\.*',
         ),
        ('\\Game\\Gear\\Weapons\\_Shared\\_Design\\_Manufacturers\\*\\_Design\\*\\*\\*Balance*\\Balance_*',
         r'\\Game\\Gear\\Weapons\\_Shared\\_Design\\_Manufacturers\\(?P<rarity_suffix>.*?)\\_Design\\(?P<guntype>.*?)\\(?P<manufacturer>.*?)\\.*',
         ),
]:

    pat = re.compile(re_pattern)
    for obj_name in data.glob(glob_pattern):

        # Skip some stuff that we probably don't want to consider
        if 'Fabricator' in obj_name:
            continue

        # Strip out some info from the object name
        suffix = None
        match = pat.match(obj_name).groupdict()
        if 'rarity_suffix' in match:
            rarity_suffix = match['rarity_suffix']

            lower = obj_name.lower()
            if 'veryrare' in lower:
                rarity = '04/Very Rare'
            elif 'rare' in lower:
                rarity = '03/Rare'
            else:
                raise Exception('Unknown rarity in {}'.format(obj_name))

            rarity = '{} {}'.format(rarity, transforms.get(rarity_suffix.lower(), rarity_suffix))
        else:
            lower = obj_name.lower()
            if 'uncommon' in lower:
                rarity = '02/Uncommon'
            elif 'common' in lower:
                rarity = '01/Common'
            elif 'veryrare' in lower:
                rarity = '04/Very Rare'
            elif 'rare' in lower:
                rarity = '03/Rare'
            elif 'firstgun' in lower:
                rarity = '01/Common (Starting Gear)'
            else:
                raise Exception('Unknown rarity in {}'.format(obj_name))

        # Now add it to our list
        gun_balances.append((
            transforms.get(match['manufacturer'].lower(), match['manufacturer']),
            transforms.get(match['guntype'].lower(), match['guntype']),
            rarity,
            obj_name,
            ))

# Sort the list so far
gun_balances.sort()

# Uniques /  Legendaries
for (label, balance_name) in [
        ("PiratesLife", '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/PiratesLife/Balance/Balance_AR_COV_Pirates'),
        ("RogueImp", '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/RogueImp/Balance/Balance_AR_COV_05_RogueImp'),
        ("LiquidCooling", '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/LiquidCooling/Balance/Balance_PS_COV_05_LiquidCoolin'),
        ]:
    gun_balances.append((
        label,
        '',
        'Named Weapon',
        balance_name,
        ))

# Shields
shield_balances = []
glob_pattern = '\\Game\\Gear\\Shields\\_Design\\InvBalance\\InvBalD_Shield_*_*_*'
pat = re.compile(r'^\\Game\\Gear\\Shields\\_Design\\InvBalance\\InvBalD_Shield_(?P<manufacturer>.*?)_(?P<rarity>\d+_.*?)$')
for obj_name in data.glob(glob_pattern):
    match = pat.match(obj_name).groupdict()
    rarity_lower = match['rarity'].lower()
    if rarity_lower == '01_common':
        rarity = '01/Common'
    elif rarity_lower == '02_uncommon':
        rarity = '02/Uncommon'
    elif rarity_lower == '03_rare':
        rarity = '03/Rare'
    elif rarity_lower == '04_veryrare':
        rarity = '04/Very Rare'
    else:
        raise Exception('Unknown rarity in {}, {}'.format(obj_name, rarity_lower))
    shield_balances.append((
        match['manufacturer'],
        'Shield',
        rarity,
        obj_name,
        ))
shield_balances.sort()
for (sname, sobj) in [
        ("InvBalD_Shield_CryingApple", '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/CryingApple/Balance/InvBalD_Shield_CryingApple'),
        ("InvBalD_Shield_ElementalAlements", '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/ElementalAlements/Balance/InvBalD_Shield_ElementalAlements'),
        ]:
    shield_balances.append((sname, 'Shield', 'Named Shield', sobj))

# Grenades
# grenade_balances = []
# glob_pattern = '/Game/Gear/GrenadeMods/_Design/InvBalance/InvBalD_GrenadeMod_*_*_*'
# pat = re.compile(r'^/Game/Gear/GrenadeMods/_Design/InvBalance/InvBalD_GrenadeMod_(?P<manufacturer>.*?)_(?P<rarity>\d+_.*?)$')
# for obj_name in data.glob(glob_pattern):
#     match = pat.match(obj_name).groupdict()
#     rarity_lower = match['rarity'].lower()
#     if rarity_lower == '01_common':
#         rarity = '01/Common'
#     elif rarity_lower == '02_uncommon':
#         rarity = '02/Uncommon'
#     elif rarity_lower == '03_rare':
#         rarity = '03/Rare'
#     elif rarity_lower == '04_veryrare':
#         rarity = '04/Very Rare'
#     else:
#         raise Exception('Unknown rarity in {}, {}'.format(obj_name, rarity_lower))
#     grenade_balances.append((
#         match['manufacturer'],
#         'Grenade',
#         rarity,
#         obj_name,
#         ))
# grenade_balances.sort()
# for (gname, gobj) in [
#         ("Acid Burn", '/Game/PatchDLC/Dandelion/Gear/Grenade/AcidBurn/Balance/InvBalD_GM_AcidBurn'),
#         ("Bloodsucker", '/Game/PatchDLC/VaultCard3/Gear/GrenadeMods/Unique/Bloodsucker/Balance/InvBalD_GM_Bloodsucker'),
#         ("Burning Summit", '/Game/Gear/GrenadeMods/_Design/_Unique/Summit/Balance/InvBalD_GM_Summit'),
#         ("Chocolate Thunder", '/Game/Gear/GrenadeMods/_Design/_Unique/JustDeserts/Balance/InvBalD_GM_JustDeserts'),
#         ("Chupa's Organ", '/Game/Gear/GrenadeMods/_Design/_Unique/Chupa/Balance/InvBalD_GM_Chupa'),
#         ("Core Buster", '/Game/PatchDLC/Geranium/Gear/Grenade/CoreBurst/Balance/InvBalD_GM_CoreBurst'),
#         ("Diamond Butt Bomb", '/Game/Gear/GrenadeMods/_Design/_Unique/ButtStallion/Balance/InvBalD_GM_ButtStallion'),
#         ("Doc Hina's Miracle Bomb", '/Game/PatchDLC/Geranium/Gear/Grenade/SkagOil/Balance/InvBalD_GM_SkagOil'),
#         ("ECHO-2", '/Game/Gear/GrenadeMods/_Design/_Unique/EchoV2/Balance/InvBalD_GM_EchoV2'),
#         ("Elemental Persistent Contact Grenade", '/Game/Gear/GrenadeMods/_Design/_Unique/Mogwai/Balance/InvBalD_GM_Mogwai'),
#         ("EMP", '/Game/Gear/GrenadeMods/_Design/_Unique/EMP/Balance/InvBalD_GM_EMP'),
#         ("Epicenter", '/Game/Gear/GrenadeMods/_Design/_Unique/Epicenter/Balance/InvBalD_GM_Epicenter'),
#         ("Exterminator", '/Game/Gear/GrenadeMods/_Design/_Unique/BirthdaySuprise/Balance/InvBalD_GM_BirthdaySuprise'),
#         ("Fastball", '/Game/Gear/GrenadeMods/_Design/_Unique/Fastball/Balance/InvBalD_GM_TED_Fastball'),
#         ("Firestorm", '/Game/Gear/GrenadeMods/_Design/_Unique/FireStorm/Balance/InvBalD_GM_VLA_FireStorm'),
#         ("Fish Slap", '/Game/PatchDLC/Event2/Gear/GrenadeMods/FishSlap/Balance/InvBalD_GM_FishSlap'),
#         ("Fungus Among Us", '/Game/Gear/GrenadeMods/_Design/_Unique/Mushroom/Balance/InvBalD_GM_Shroom'),
#         ("Ghast Call", '/Game/PatchDLC/BloodyHarvest/Gear/GrenadeMods/_Design/_Unique/FontOfDarkness/Balance/InvBalD_GM_TOR_FontOfDarkness'),
#         ("Hex", '/Game/Gear/GrenadeMods/_Design/_Unique/Seeker/Balance/InvBalD_GM_Seeker'),
#         ("HOT Spring", '/Game/PatchDLC/Ixora/Gear/GrenadeMods/HOTSpring/Balance/InvBalD_GM_HOTSpring'),
#         ("Hunter-Seeker", '/Game/Gear/GrenadeMods/_Design/_Unique/HunterSeeker/Balance/InvBalD_GM_HunterSeeker'),
#         ("It's Piss", '/Game/Gear/GrenadeMods/_Design/_Unique/Piss/Balance/InvBalD_GM_Piss'),
#         ("Kryll", '/Game/Gear/GrenadeMods/_Design/_Unique/Kryll/Balance/InvBalD_GM_Kryll'),
#         ("Lightspeed", '/Game/PatchDLC/Takedown2/Gear/GrenadeMods/Lightspeed/Balance/InvBalD_GM_HYP_Lightspeed'),
#         ("Mesmer", '/Game/PatchDLC/Ixora2/Gear/GrenadeMods/_Unique/Mesmer/Balance/InvBalD_GM_Mesmer'),
#         ("Moxxi's Bouncing Pair", '/Game/Gear/GrenadeMods/_Design/_Unique/MoxiesBosom/Balance/InvBalD_GM_PAN_MoxiesBosom'),
#         ("Nagata", '/Game/Gear/GrenadeMods/_Design/_Unique/Nagate/Balance/InvBalD_GM_Nagate'),
#         ("NOG Potion #9", '/Game/Gear/GrenadeMods/_Design/_Unique/WizardOfNOG/Balance/InvBalD_GM_WizardOfNOG'),
#         ("Porcelain Pipe Bomb", '/Game/Gear/GrenadeMods/_Design/_Unique/ToiletBombs/Balance/InvBalD_GM_TOR_ToiletBombs'),
#         ("Pyroburst", '/Game/PatchDLC/VaultCard2/Gear/GrenadeMods/Unique/Pyroburst/Balance/InvBalD_GM_Pyroburst'),
#         ("Quasar", '/Game/Gear/GrenadeMods/_Design/_Unique/Quasar/Balance/InvBalD_GM_Quasar'),
#         ("Red Queen", '/Game/Gear/GrenadeMods/_Design/_Unique/RedQueen/Balance/InvBalD_GM_RedQueen'),
#         ("Ringer / The Big Ringer / Dead Ringer", '/Game/PatchDLC/Ixora2/Gear/GrenadeMods/_Unique/Ringer/Balance/InvBalD_GM_Ringer'),
#         ("Rubber Cheddar Shredder", '/Game/Gear/GrenadeMods/_Design/_Unique/CashMoneyPreorder/Balance/InvBalD_GM_CashMoneyPreorder'),
#         ("Sidewinder", '/Game/PatchDLC/VaultCard3/Gear/GrenadeMods/Unique/Sidewinder/Balance/InvBalD_GM_Sidewinder'),
#         ("Slider", '/Game/PatchDLC/Dandelion/Gear/Grenade/Slider/Balance/InvBalD_GM_TED_Slider'),
#         ("Storm Front", '/Game/Gear/GrenadeMods/_Design/_Unique/StormFront/Balance/InvBalD_GM_StormFront'),
#         ("Surge", '/Game/Gear/GrenadeMods/_Design/_Unique/Surge/Balance/InvBalD_GM_Surge'),
#         ("Tina's Hippity Hopper", '/Game/Gear/GrenadeMods/_Design/_Unique/HipHop/Balance/InvBalD_GM_TOR_HipHop'),
#         ("Tran-fusion", '/Game/Gear/GrenadeMods/_Design/_Unique/TranFusion/Balance/InvBalD_GM_TranFusion'),
#         ("Ultraball", '/Game/Gear/GrenadeMods/_Design/_Unique/ToyGrenade/Balance/InvBalD_GM_ToyGrenade'),
#         ("Whispering Ice", '/Game/Gear/GrenadeMods/_Design/_Unique/ObviousTrap/Balance/InvBalD_GM_ObviousTrap'),
#         ("Widowmaker", '/Game/Gear/GrenadeMods/_Design/_Unique/WidowMaker/Balance/InvBalD_GM_WidowMaker'),
#         ]:
#     grenade_balances.append((gname, 'Grenade', 'Named Grenade', gobj))

# COMs
char_map = {
        'BSM': 'Beastmaster',
        }
com_balances = []
for glob_pattern, re_pat, extra_label in [
        ('\\Game\\Gear\\Pauldrons\\_Shared\\_Design\\Balance\\Balance_Armor_*_*',
            r'^\\Game\\Gear\\Pauldrons\\_Shared\\_Design\\Balance\\Balance_Armor_(?P<rarity>\d+_.*?)$',
            None),
        ]:
    # pat = re.compile(r'^\\Game\\Gear\\Shields\\_Design\\InvBalance\\InvBalD_Shield_(?P<manufacturer>.*?)_(?P<rarity>\d+_.*?)$')
    pat = re.compile(re_pat)
    for obj_name in data.glob(glob_pattern):
        temp = pat.match(obj_name)
        match = pat.match(obj_name).groupdict()
        rarity_lower = match['rarity'].lower()
        if rarity_lower == '01_common':
            rarity = '01/Common'
        elif rarity_lower == '02_uncommon':
            rarity = '02/Uncommon'
        elif rarity_lower == '03_rare':
            rarity = '03/Rare'
        elif rarity_lower == '04_veryrare':
            rarity = '04/Very Rare'
        elif rarity_lower == '05_legendary':
            rarity = '05/Legendary'
        else:
            raise Exception('Unknown rarity in {}, {}'.format(obj_name, rarity_lower))
        com_balances.append((
            'All',
            'Pauldrons',
            rarity,
            obj_name,
            ))
# Base-game Legendary COMs as dropped by Trials Bosses (as of M4/Maliwan Takedown) update
for (cname, cobj) in [
        ('Balance_Armor_Amalgam', '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Amalgam/Balance/Balance_Armor_Amalgam'),
        ('Balance_Armor_BigBMittens', '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/BigBMittens/Balance/Balance_Armor_BigBMittens'),
        ]:
    com_balances.append((cname, 'Class Mod', 'Pauldron', cobj))
com_balances.sort()

# Artifacts
# artifact_balances_base = [
#         ('Common', 'Artifact', '01/Common', '/Game/Gear/Artifacts/_Design/BalanceDefs/InvBalD_Artifact_01_Common'),
#         ('Uncommon', 'Artifact', '02/Uncommon', '/Game/Gear/Artifacts/_Design/BalanceDefs/InvBalD_Artifact_02_Uncommon'),
#         ('Rare', 'Artifact', '03/Rare', '/Game/Gear/Artifacts/_Design/BalanceDefs/InvBalD_Artifact_03_Rare'),
#         ('Very Rare', 'Artifact', '04/Very Rare', '/Game/Gear/Artifacts/_Design/BalanceDefs/InvBalD_Artifact_04_VeryRare'),
#         ('Legendary', 'Artifact', '05/Legendary', '/Game/Gear/Artifacts/_Design/BalanceDefs/InvBalD_Artifact_05_Legendary'),
#         ]
# artifact_balances_legendary = [
#         # Not bothering to do anything fancy here since there's so few.
#         ("Company Man (Atlas)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Atlas/Balance/InvBalD_Artifact_CompanyMan_Atlas'),
#         ("Company Man (CoV)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/CoV/Balance/InvBalD_Artifact_CompanyMan_CoV'),
#         ("Company Man (Dahl)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Dahl/Balance/InvBalD_Artifact_CompanyMan_Dahl'),
#         ("Company Man (Hyperion)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Hyperion/Balance/InvBalD_Artifact_CompanyMan_Hyperion'),
#         ("Company Man (Jakobs)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Jakobs/Balance/InvBalD_Artifact_CompanyMan_Jakobs'),
#         ("Company Man (Maliwan)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Maliwan/Balance/InvBalD_Artifact_CompanyMan_Maliwan'),
#         ("Company Man (Tediore)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Tediore/Balance/InvBalD_Artifact_CompanyMan_Tediore'),
#         ("Company Man (Torgue)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Torgue/Balance/InvBalD_Artifact_CompanyMan_Torgue'),
#         ("Company Man (Vladof)", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/CompanyMan/Vladof/Balance/InvBalD_Artifact_CompanyMan_Vladof'),
#         ("Deathrattle", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora/Gear/Artifacts/_Design/_Unique/Deathrattle/Balance/InvBalD_Artifact_Deathrattle'),
#         ("Electric Banjo", 'Artifact', '05/Legendary', '/Game/Gear/Artifacts/_Design/PartSets/Abilities/_Unique/ElectricBanjo/Balance/InvBalD_Artifact_ElectricBanjo'),
#         ("Grave", 'Artifact', '05/Legendary', '/Game/Gear/Artifacts/_Design/PartSets/Abilities/_Unique/Grave/Balance/InvBalD_Artifact_Grave'),
#         ("Holy Grail", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora/Gear/Artifacts/_Design/_Unique/HolyGrail/Balance/InvBalD_Artifact_HolyGrail'),
#         ("Lunacy", 'Artifact', '05/Legendary', '/Game/PatchDLC/Hibiscus/Gear/Artifacts/_Design/_Unique/Lunacy/Balance/InvBalD_Artifact_Lunacy'),
#         ("Mysterious Amulet", 'Artifact', '04/Very Rare', '/Game/PatchDLC/Ixora/Gear/Artifacts/_Design/_Unique/MysteriousAmulet/Balance/InvBalD_Artifact_MysteriousAmulet'),
#         ("Mysterious Artifact", 'Artifact', '04/Very Rare', '/Game/PatchDLC/Ixora2/Gear/Artifacts/_Unique/MysteriousAmulet/Balance/InvBalD_Artifact_MysteriousAmulet'),
#         ("Pearl of Ineffable Knowledge", 'Artifact', '05/Legendary', '/Game/PatchDLC/Hibiscus/Gear/Artifacts/_Design/_Unique/PUK/Balance/InvBalD_Artifact_PUK'),
#         ("Phoenix Tears", 'Artifact', '05/Legendary', '/Game/Gear/Artifacts/_Design/PartSets/Abilities/_Unique/PhoenixTears/Balance/InvBalD_Artifact_PhoenixTears'),
#         ("Road Warrior", 'Artifact', '05/Legendary', '/Game/Gear/Artifacts/_Design/PartSets/Abilities/_Unique/RoadWarrior/Balance/InvBalD_Artifact_RoadWarrior'),
#         ("Shlooter", 'Artifact', '05/Legendary', '/Game/PatchDLC/VaultCard2/Gear/Artifacts/Unique/Shlooter/Balance/InvBalD_Artifact_Shlooter'),
#         ("Toboggan", 'Artifact', '05/Legendary', '/Game/PatchDLC/Ixora/Gear/Artifacts/_Design/_Unique/Toboggan/Balance/InvBalD_Artifact_Toboggan'),
#         ("Unleash the Dragon", 'Artifact', '05/Legendary', '/Game/Gear/Artifacts/_Design/PartSets/Abilities/_Unique/ElDragonJr/Balance/InvBalD_Artifact_ElDragonJr'),
#         ("Vault Hunter's Relic", 'Artifact', '05/Legendary', '/Game/Gear/Artifacts/_Design/PartSets/Abilities/_Unique/VaultHunterRelic/Balance/InvBalD_Artifact_Relic'),
#         ("Vendetta", 'Artifact', '04/Very Rare', '/Game/PatchDLC/Geranium/Gear/Artifacts/_Design/_Unique/Vengeance/Balance/InvBalD_Artifact_Vengeance'),
#         ]
# # "Specific" Legendary Artifact balances added by Raid1
# for (aname, aobj) in [
#         ("Commander Planetoid", '/Game/PatchDLC/Raid1/Gear/Artifacts/CommanderPlanetoid/InvBalD_Artifact_CommanderPlanetoid'),
#         ("Cosmic Crater", '/Game/PatchDLC/Raid1/Gear/Artifacts/CosmicCrater/InvBalD_Artifact_CosmicCrater'),
#         ("Deathless", '/Game/PatchDLC/Raid1/Gear/Artifacts/Deathless/InvBalD_Artifact_Deathless'),
#         ("Launch Pad", '/Game/PatchDLC/Raid1/Gear/Artifacts/Salvo/InvBalD_Artifact_Salvo'),
#         ("Loaded Dice", '/Game/PatchDLC/Raid1/Gear/Artifacts/LoadedDice/InvBalD_Artifact_LoadedDice'),
#         ("Moxxi's Endowment", '/Game/PatchDLC/Raid1/Gear/Artifacts/MoxxisEndowment/InvBalD_Artifact_MoxxisEndowment'),
#         ("Otto Idol", '/Game/PatchDLC/Raid1/Gear/Artifacts/OttoIdol/InvBalD_Artifact_OttoIdol'),
#         ("Pull Out Method", '/Game/PatchDLC/Raid1/Gear/Artifacts/PullOutMethod/InvBalD_Artifact_PullOutMethod'),
#         ("Rocket Boots", '/Game/PatchDLC/Raid1/Gear/Artifacts/RocketBoots/InvBalD_Artifact_RocketBoots'),
#         ("Safeguard", '/Game/PatchDLC/Raid1/Gear/Artifacts/Safegaurd/InvBalD_Artifact_Safegaurd'),
#         ("Splatter Gun", '/Game/PatchDLC/Raid1/Gear/Artifacts/SplatterGun/InvBalD_Artifact_SplatterGun'),
#         ("Static Charge", '/Game/PatchDLC/Raid1/Gear/Artifacts/StaticTouch/InvBalD_Artifact_StaticTouch'),
#         ("Victory Rush", '/Game/PatchDLC/Raid1/Gear/Artifacts/VictoryRush/InvBalD_Artifact_VictoryRush'),
#         ("White Elephant", '/Game/PatchDLC/Raid1/Gear/Artifacts/WhiteElephant/InvBalD_Artifact_WhiteElephant'),
#         ]:
#     artifact_balances_legendary.append((
#         '{} (dedicated drop only)'.format(aname),
#         'Artifact',
#         '05/Legendary',
#         aobj,
#         ))
# artifact_balances_legendary.sort()
# artifact_balances = artifact_balances_base + artifact_balances_legendary

# Loop through
part_cache = {}
title_cache = {}
for (filename, filename_long, balances, man_col_name, type_col_name, partset_names) in [
        ('gun_balances.csv', 'gun_balances_long.csv', gun_balances, 'Manufacturer/Name', 'Gun Type', None),
        ('shield_balances.csv', 'shield_balances_long.csv', shield_balances, 'Manufacturer/Name', None, [
            'BODY',
            'RARITY',
            'LEGENDARY AUG',
            'AUGMENT',
            'ELEMENT',
            'MATERIAL',
            ]),
        ('com_balances.csv', 'com_balances_long.csv', com_balances, 'Character/Name', None, [
            'MODTYPE',
            'RARITY',
            'PRIMARY',
            'SECONDARY',
            'SKILLS',
            '(unknown)',
            ]),
        ]:

    print('Processing {}'.format(filename))
    with open(filename, 'w') as odf:
        with open(filename_long, 'w') as odf_long:

            writer = csv.writer(odf)
            writer_long = csv.writer(odf_long)
            header = [man_col_name]
            if type_col_name:
                header.append(type_col_name)
            header.extend([
                'Rarity',
                'Balance',
                'Category',
                'Min Parts',
                'Max Parts',
                'Weight',
                'Part',
                'Dependencies',
                'Excluders',
                ])
            writer.writerow(header)
            writer_long.writerow(header)

            for manufacturer, gun_type, rarity, bal_name in balances:

                # Grab a Balance object
                bal = Balance.from_data(data, bal_name)

                # Quick check...  Thus far all examples of this also have the manufacturers enumerated in the
                # parts list, so probably we don't need to worry.
                # (actually just commenting this for now)
                #if len(bal.raw_bal_data['Manufacturers']) > 1:
                #    # Excluding reporting for the ones that I've already looked at
                #    if bal_name not in {
                #            '/Game/Gear/GrenadeMods/_Design/_Unique/Chupa/Balance/InvBalD_GM_Chupa',
                #            '/Game/Gear/GrenadeMods/_Design/_Unique/FireStorm/Balance/InvBalD_GM_VLA_FireStorm',
                #            '/Game/Gear/GrenadeMods/_Design/_Unique/Quasar/Balance/InvBalD_GM_Quasar',
                #            '/Game/Gear/GrenadeMods/_Design/_Unique/StormFront/Balance/InvBalD_GM_StormFront',
                #            '/Game/Gear/GrenadeMods/_Design/_Unique/TranFusion/Balance/InvBalD_GM_TranFusion',
                #            '/Game/Gear/GrenadeMods/_Design/_Unique/WidowMaker/Balance/InvBalD_GM_WidowMaker',
                #            }:
                #        print('WARNING: {} has {} manufacturers'.format(bal_name, len(bal.raw_bal_data['Manufacturers'])))

                # Loop through partlists
                seen_labels = set()
                for apl_idx, category in enumerate(bal.categories):

                    # Check for multiple-part selection
                    if category.select_multiple:
                        parts_min = category.num_min
                        parts_max = category.num_max
                        # Some items (such as the Storm Front grenade) have a bunch of parts defined
                        # in a multi-select category but have Min/Max of 0.  These parts are never
                        # actually selected, so ignore 'em.
                        if parts_min == 0 and parts_max == 0:
                            # Turns out there's a few guns too, but those rows were already getting pruned later.
                            #print('Skipping category {} for {}; zero min/max on multi-select'.format(apl_idx, partset_name))
                            continue
                    else:
                        parts_min = 1
                        parts_max = 1

                    processed_parts = []

                    for part_idx, part in enumerate(category.partlist):

                        part_name = part.part_name
                        weight = data.process_bvc(part.weight)

                        # Populate the cache, if we need to
                        if part_name not in part_cache:
                            if part_name == 'None':
                                part_cache[part_name] = (set(), set())
                            else:
                                excluders = set()
                                dependencies = set()
                                part_data = data.get_data(part_name)
                                found_export = False

                                for export in part_data:
                                    if export['export_type'].startswith('BPInvPart_'):
                                        found_export = True
                                        if 'Excluders' in export:
                                            for excluder in export['Excluders']:
                                                if 'export' in excluder:
                                                    # WTF is going on here?  So far, this object seems to just reference *itself* in here?
                                                    # /Game/Gear/Shields/_Design/PartSets/Part_Augment/Safespace/Part_Shield_Aug_Knockback
                                                    # Just gonna print a warning, though I'm excluding notifications for the ones that I've
                                                    # looked at and don't actually care about. :)
                                                    if part_name not in {
                                                            '/Game/Gear/Shields/_Design/PartSets/Part_Augment/Safespace/Part_Shield_Aug_Knockback',
                                                            '/Game/Gear/Shields/_Design/_Uniques/Revengenader/Parts/Part_Shield_Aug_PAN_LGD_Revengenader',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_ActionSkillCooldownRate',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_MeleeDamage',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_HealthMax',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_HealthRegen',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_ShieldCapacity',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_ShieldRegenDelay',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_ShieldRegenRate',
                                                            '/Game/Gear/ClassMods/_Design/PartSets/Part_Stats/Part_Primary_Stat/ClassMod_Part_Stat_Primary_ActionSkillDamage',
                                                            }:
                                                        print('WARNING: {} Excluders references itself?'.format(part_name))
                                                else:
                                                    excluders.add(excluder[1])
                                        if 'Dependencies' in export:
                                            for dependency in export['Dependencies']:
                                                dependencies.add(dependency[1])

                                        break
                                if not found_export:
                                    raise Exception('Could not find export for {}'.format(part_name))

                                part_cache[part_name] = (excluders, dependencies)

                        # Read from Cache
                        (excluders, dependencies) = part_cache[part_name]
                        processed_parts.append((part_name, excluders, dependencies, weight))

                    # If we have no parts, skip it
                    if len(processed_parts) == 0:
                        continue

                    # Special case!  A partset with literally just *one* part, with a name of None.
                    # No reason to show this, has no actual bearing on the weapon.
                    if len(processed_parts) == 1 and processed_parts[0][0] == 'None':
                        continue

                    # if bal_name == '\Game\Gear\Shields\_Design\InvBalance\InvBalD_Shield_Anshin_01_Common':
                    #     print('ok')
                    # Figure out what the main label should be for this part type
                    label_text = data.get_parts_category_name([p[0] for p in processed_parts], bal_name, apl_idx)

                    # Hardcoded fixes.  Grr.
                    if label_text is None:
                        if bal.partset_name == '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Nurf/Balance/PartSet_PS_TOR_Nurf' and apl_idx == 1:
                            # BODY ACCESSORY vs. BARREL ACCESSORY
                            label_text = 'BODY ACCESSORY'
                        elif bal.partset_name == '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/Ogre/Balance/InvPart_VLA_AR_Ogre' and apl_idx == 10:
                            # IRON SIGHTS vs. RAIL
                            label_text = 'RAIL'
                        else:
                            raise Exception('Possible contention (or unknowns) in {}, APL {}'.format(bal_name, apl_idx))

                    # Make sure we're not re-using a label
                    if len(processed_parts) > 0:
                        idx = 1
                        label_base = label_text
                        while label_text in seen_labels:
                            idx += 1
                            label_text = '{} {}'.format(label_base, idx)
                        seen_labels.add(label_text)

                    for (part_name, excluders, dependencies, weight) in processed_parts:
                        datarow = [manufacturer]
                        datarow_long = [manufacturer]
                        if type_col_name:
                            datarow.append(gun_type)
                            datarow_long.append(gun_type)

                        # Shortly before the April 8, 2021 patch, I updated my serialization pipeline a bit,
                        # which resulted in weights getting reported as always floats, even if the weight was
                        # 1 (so they'd be 1.0).  I always check diffs of the newly-generated CSVs after adding
                        # new data, to make sure that nothing weird has happened, and this int->float reporting
                        # made doing so difficult.  So we'll check the rounding value and fudge it.
                        if round(weight, 6) == int(weight):
                            weight = int(weight)

                        # The DLC6 patch introduced a "Mysterious Artifact," which looks identical to
                        # the "Mysterious Amulet" introduced in the DLC5 patch, and has the same "short" name.
                        # We're going to report the full path for these, rather than just the short name,
                        # because otherwise it'd be impossible to know which one we're referring to.  Do this
                        # for the individual part, as well.
                        if 'InvBalD_Artifact_MysteriousAmulet' in bal_name:
                            bal_name_report = bal_name
                        else:
                            bal_name_report = bal_name.split('/')[-1]
                        if 'Artifact_Part_Ability_MysteriousAmulet' in part_name:
                            part_name_report = part_name
                        else:
                            part_name_report = part_name.split('/')[-1]

                        # Write out to our "main" CSV
                        datarow.extend([
                            rarity,
                            bal_name_report,
                            label_text,
                            parts_min,
                            parts_max,
                            weight,
                            part_name_report,
                            ', '.join(sorted([d.split('/')[-1] for d in dependencies])),
                            ', '.join(sorted([e.split('/')[-1] for e in excluders])),
                            ])
                        writer.writerow(datarow)

                        # Write out to an alternate "long" CSV (used by bl3-cli-saveedit mostly)
                        datarow_long.extend([
                            rarity,
                            bal_name,
                            label_text,
                            parts_min,
                            parts_max,
                            weight,
                            part_name,
                            ', '.join(sorted(dependencies)),
                            ', '.join(sorted(excluders)),
                            ])
                        writer_long.writerow(datarow_long)

            print('... done!')

