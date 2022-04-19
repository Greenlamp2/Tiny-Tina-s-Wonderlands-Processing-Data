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
    ("IntroMission", '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/IntroMission/Balance/Balance_DAL_PS_FirstGun'),
    ("TheHost", '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/TheHost/Balance/Balance_PS_Tediore_05_TheHost'),
    ("ThrowableHole", '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/ThrowableHole/Balance/Balance_SM_TED_05_ThrowableHole'),
    ("FragmentRain", '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/FragmentRain/Balance/Balance_SM_TED_05_FragmentRain'),
    ("HawkinsWrath", '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/HawkinsWrath/Balance/Balance_SG_Torgue_05_HawkinsWrath'),
    ("Catatumbo", '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Catatumbo/Balance/Balance_PS_JAK_05_Catatumbo'),
    ("ReignOfArrows", '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/ReignOfArrows/Balance/Balance_SG_JAK_05_ReignOfArrows'),
    ("WhiteRider", '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/WhiteRider/Balance/Balance_SM_DAHL_05_WhiteRider'),
    ("LiveWire", '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/LiveWire/Balance/Balance_SM_DAHL_05_LiveWire'),
    ("BlazingVolley", '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/BlazingVolley/Balance/Balance_SM_HYP_05_BlazingVolley'),
    ("Swordsplosion", '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordsplosion/Balance/Balance_SG_Torgue_05_Swordsplosion'),
    ("RogueImp", '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/RogueImp/Balance/Balance_AR_COV_05_RogueImp'),
    ("CrossGen", '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/_Unique/CrossGen/Balance/Balance_AR_JAK_05_CrossGen'),
    ("BreadSlicer", '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/BreadSlicer/Balance/Balance_AR_VLA_05_BreadSlicer'),
    ("Cannonballer", '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Cannonballer/Balance/Balance_HW_TOR_05_Cannonballer'),
    ("LiquidCooling", '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/LiquidCooling/Balance/Balance_PS_COV_05_LiquidCoolin'),
    ("Gluttony", '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/Gluttony/Balance/Balance_PS_Tediore_05_Gluttony'),
    ("RedHellion", '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/RedHellion/Balance/Balance_SG_HYP_05_RedHellion'),
    ("CrossBlade", '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/CrossBlade/Balance/Balance_SG_JAK_05_Crossblade'),
    ("WizardPipe", '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/WizardPipe/Balance/Balance_SM_HYP_05_WizardsPipe'),
    ("ThunderAnima", '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/ThunderAnima/Balance/Balance_AR_COV_ThunderAni'),
    ("QuadBow", '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/QuadBow/Balance/Balance_DAL_AR_Quadbow'),
    ("Donkey", '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/Donkey/Balance/Balance_AR_VLA_Donkey'),
    ("Perceiver", '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Perceiver/Balance/Balance_DAL_PS_05_Perceiver'),
    ("MasterworkCrossbow", '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/MasterworkCrossbow/Balance/Balance_PS_JAK_MasterworkCrossbow'),
    ("QueensCry", '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/QueensCry/Balance/Balance_PS_VLA_QueensCry'),
    ("Envy", '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Envy/Balance/Balance_SR_JAK_05_Envy'),
    ("BlueCake", '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/BlueCake/Balance/Balance_HW_COV_05_BlueCake'),
    ("Message", '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Message/Balance/Balance_PS_TOR_05_Message'),
    ("AUTOMAGICEXE", '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/AUTOMAGICEXE/Balance/Balance_PS_VLA_05_AUTOMAGICEXE'),
    ("SkeepProd", '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/_Unique/SkeepProd/Balance/Balance_SR_DAL_05_SkeepProd'),
    ("DrylsFury", '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/DrylsFury/Balance/Balance_VLA_SR_05_DrylsFury'),
    ("Apex", '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Apex/Balance/Balance_DAL_PS_05_Apex'),
    ("AntGreatBow", '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow'),
    ("AntGreatBow", '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow_Used'),
    ("Carrouser", '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Carrouser/Balance/Balance_SR_JAK_05_Carrouser'),
    ("PortableSawmill", '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/PortableSawmill/Balance/Balance_VLA_SR_05_PortableSawmill'),
    ("RoisensSpite", '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/RoisensSpite/Balance/Balance_DAL_PS_RoisensSpite'),
    ("CircGyre", '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/CircGyre/Balance/Balance_SG_HYP_05_CircGuire'),
    ("Sworderang", '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/Sworderang/Balance/Balance_SG_Tediore_05_Sworderang'),
    ("BoreasBreath", '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/BoreasBreath/Balance/Balance_SM_TED_BoreasBreath'),
    ("Shadowfire", '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/Shadowfire/Balance/Balance_SM_TED_05_Shadowfire'),
    ("PiratesLife", '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/PiratesLife/Balance/Balance_AR_COV_Pirates'),
    ("DreadLord", '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/DreadLord/Balance/Balance_AR_VLA_Dreadlord'),
    ("Birthright", '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/Birthright/Balance/Balance_PS_VLA_Birthright'),
    ("Anchor", '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Anchor/Balance/Balance_HW_TOR_Anchor'),
    ("DrylsLegacy", '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/DrylsLegacy/Balance/Balance_SM_HYP_05_DrylsLegacy'),
    ("Tootherator", '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/Tootherator/Balance/Balance_SR_HYP_03_Tootherator'),
    ("Moleman", '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/_Unique/Moleman/Balance/Balance_HW_VLA_04_Moleman'),
    ("Heckwader", '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/Heckwader/Balance/Balance_SM_DAL_Heckwader'),
    ("Diplomacy", '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Diplomacy/Balance/Balance_SG_Torgue_05_Diplomacy'),
    ("Pookie", '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Pookie/Balance/Balance_PS_JAK_05_Pookie'),
    ("Headcannon", '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Headcannon/Balance/Balance_PS_TOR_05_Headcannon'),
    ("Repellant", '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/Repellant/Balance/Balance_PS_COV_05_Repellant'),
    ("IronSides", '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/IronSides/Balance/Balance_SR_JAK_05_IronSides'),
    ("Mistrial", '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/Mistrial/Balance/Balance_DAL_AR_Mistrial'),
    ("LastRites", '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/LastRites/Balance/Balance_SG_HYP_05_LastRites'),
    ("LovePanther", '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/LovePanther/Balance/Balance_HW_COV_05_LovePanther'),
    ("KaoKhan", '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/KaoKhan/Balance/Balance_SR_HYP_KaoKhan'),
    ("ManualTransmission", '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Balance/Balance_AR_VLA_ManualTrans'),
    ("Swordruption", '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordruption/Balance/Balance_SG_Torgue_Swordruption'),
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
    ("CryingApple", '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/CryingApple/Balance/InvBalD_Shield_CryingApple'),
    ("ElementalAlements", '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/ElementalAlements/Balance/InvBalD_Shield_ElementalAlements'),
    ("RonRivote", '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/RonRivote/Balance/InvBalD_Shield_RonRivote'),
    ("PowerNap", '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/PowerNap/Balance/InvBalD_Shield_PowerNap'),
    ("TwistedSisters", '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/TwistedSisters/Balance/InvBalD_Shield_TwistedSisters'),
    ("Vamp", '/Game/Gear/Shields/_Design/_Uniques/Vamp/Balance/InvBalD_Shield_Legendary_Vamp'),
    ("Rune_Spirit", '/Game/Gear/Shields/_Design/_Uniques/Rune_Spirit/Balance/InvBalD_Shield_SpiritRune'),
    ("Rune_Body", '/Game/Gear/Shields/_Design/_Uniques/Rune_Body/Balance/InvBalD_Shield_Rune_Body'),
    ("Rune_Mind", '/Game/Gear/Shields/_Design/_Uniques/Rune_Mind/Balance/InvBalD_Shield_Rune_Mind'),
    ("HammerAnvil", '/Game/Gear/Shields/_Design/_Uniques/HammerAnvil/Balance/InvBalD_Shield_HammerAnvil'),
    ("Rune_Master", '/Game/Gear/Shields/_Design/_Uniques/Rune_Master/Balance/InvBalD_Shield_Rune_Master'),
    ("FullBattery", '/Game/Gear/Shields/_Design/_Uniques/FullBattery/Balance/InvBalD_Shield_FullBattery'),
    ("UndeadPact", '/Game/Gear/Shields/_Design/_Uniques/UndeadPact/Balance/InvBalD_Shield_UndeadPAct'),
    ("CursedWit", '/Game/Gear/Shields/_Design/_Uniques/CursedWit/Balance/InvBalD_Shield_CursedWit'),
    ("Afterburner", '/Game/Gear/Shields/_Design/_Uniques/Afterburner/Balance/InvBalD_Shield_Afterburner'),
    ("AncientDeity", '/Game/Gear/Shields/_Design/_Uniques/AncientDeity/Balance/InvBalD_Shield_AncientDeity'),
    ("BadEgg", '/Game/Gear/Shields/_Design/_Uniques/BadEgg/Balance/InvBalD_Shield_BadEgg'),
    ("BroncoBuster", '/Game/Gear/Shields/_Design/_Uniques/BroncoBuster/Balance/InvBalD_Shield_BroncoBuster'),
    ("KineticFriction_Health", '/Game/Gear/Shields/_Design/_Uniques/KineticFriction_Health/Balance/InvBalD_Shield_KineticFriction_Health'),
    ("KineticFriction_Shield", '/Game/Gear/Shields/_Design/_Uniques/KineticFriction_Shield/Balance/InvBalD_Shield_KineticFriction_Shield'),
    ("LastGasp", '/Game/Gear/Shields/_Design/_Uniques/LastGasp/Balance/InvBalD_Shield_LastGasp'),
    ("MacedWard", '/Game/Gear/Shields/_Design/_Uniques/MacedWard/Balance/InvBalD_Shield_MacedWard'),
    ("Shamwai", '/Game/Gear/Shields/_Design/_Uniques/Shamwai/Balance/InvBalD_Shield_Shamwai'),
    ("Transistor", '/Game/Gear/Shields/_Design/_Uniques/Transistor/Balance/InvBalD_Shield_Transistor'),
    ("TrickMirror", '/Game/Gear/Shields/_Design/_Uniques/TrickMirror/Balance/InvBalD_Shield_TrickMirror'),
]:
    shield_balances.append((sname, 'Shield', 'Named Shield', sobj))

#Pauldrons
com_balances = []
for glob_pattern, re_pat, extra_label in [
        ('\\Game\\Gear\\Pauldrons\\_Shared\\_Design\\Balance\\Balance_Armor_*_*',
            r'^\\Game\\Gear\\Pauldrons\\_Shared\\_Design\\Balance\\Balance_Armor_(?P<rarity>\d+_.*?)$',
            None),
        ]:
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
            '',
            'Pauldron',
            rarity,
            obj_name,
            ))

for (cname, cobj) in [
    ("SelectiveAmnesia", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SelectiveAmnesia/Balance/Balance_Armor_SelectiveAmnesia'),
    ("Claw", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Claw/Balance/Balance_Armor_MantisClaw'),
    ("DiamondGauntlets", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DiamondGauntlets/Balance/Balance_Armor_DiamondGauntlets'),
    ("HeadOfTheSnake", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/HeadOfTheSnake/Balance/Balance_Armor_HeadOfTheSnake'),
    ("Pandemecium", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Pandemecium/Balance/Balance_Armor_Pandemecium'),
    ("SmartArmor", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SmartArmor/Balance/Balance_Armor_SmartArmor'),
    ("SteelGauntlets", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SteelGauntlets/Balance/Balance_Armor_SteelGauntlets'),
    ("CorruptedPlatemail", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/CorruptedPlatemail/Balance/Balance_Armor_CorruptedPlatemail'),
    ("DeathlessMantle", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DeathlessMantle/Balance/Balance_Armor_DeathlessMantle'),
    ("Amalgam", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Amalgam/Balance/Balance_Armor_Amalgam'),
    ("BigBMittens", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/BigBMittens/Balance/Balance_Armor_BigBMittens'),
    ("Tabula", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Tabula/Balance/Balance_Armor_Tabula'),
]:
    com_balances.append((cname, 'Pauldron', 'Named Pauldron', cobj))
com_balances.sort()

#Amulets
amu_balances = []
for glob_pattern, re_pat, extra_label in [
        ('\\Game\\Gear\\Amulets\\_Shared\\_Design\\Balance\\Balance_Amulets_*_*',
            r'^\\Game\\Gear\\Amulets\\_Shared\\_Design\\Balance\\Balance_Amulets_(?P<rarity>\d+_.*?)$',
            None),
        ]:
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
        amu_balances.append((
            '',
            'Amulet',
            rarity,
            obj_name,
            ))

for (cname, cobj) in [
    ("BlazeOfGlory", '/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Balance/Balance_Amulet_Unique_BlazeOfGlory'),
    ("Frenzied", '/Game/Gear/Amulets/_Shared/_Unique/Frenzied/Balance/Balance_Amulet_Unique_Frenzied'),
    ("GTFO", '/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO'),
    ("RonRivote", '/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote'),
    ("JointTraining", '/Game/Gear/Amulets/_Shared/_Unique/JointTraining/Balance/Balance_Amulet_Unique_JointTraining'),
    ("Bradluck", '/Game/Gear/Amulets/_Shared/_Unique/Bradluck/Balance/Balance_Amulet_Unique_Bradluck'),
    ("UniversalSoldier", '/Game/Gear/Amulets/_Shared/_Unique/UniversalSoldier/Balance/Balance_Amulet_Unique_UniversalSoldier'),
    ("Harbinger", '/Game/Gear/Amulets/_Shared/_Unique/Harbinger/Balance/Balance_Amulet_Unique_Harbinger'),
    ("Theruge", '/Game/Gear/Amulets/_Shared/_Unique/Theruge/Balance/Balance_Amulet_Unique_Theruge'),
    ("HarmoniousDingleDangle", '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb'),
    ("HarmoniousDingleDangle", '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage'),
    ("HarmoniousDingleDangle", '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC'),
    ("HarmoniousDingleDangle", '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro'),
    ("HarmoniousDingleDangle", '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger'),
    ("HarmoniousDingleDangle", '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue'),
]:
    amu_balances.append((cname, 'Amulet', 'Named Amulet', cobj))
amu_balances.sort()

#Melee
melee_balances = []
for glob_pattern, re_pat, extra_label in [
        ('\\Game\\Gear\\Melee\\_Shared\\_Design\\Balance\\Balance_M_*_*',
            r'^\\Game\\Gear\\Melee\\_Shared\\_Design\\Balance\\Balance_M_(?P<type>.*?)_(?P<rarity>\d+_.*?)$',
            None),
        ]:
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
        melee_balances.append((
            'Melee',
            match['type'],
            rarity,
            obj_name,
            ))

for (cname, cobj) in [
    ("SmithCharade", '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_MissionWeapon'),
    ("IntroMission", '/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission'),
    ("IntroMission", '/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission_SkellySword'),
    ("PaladinSword", '/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/PaladinSword/Balance/Balance_M_Sword2H_PaladinSword'),
    ("BodySpray", '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/BodySpray/Balance/Balance_M_Axe_BodySpray'),
    ("Tidesorrow", '/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow/Balance/Balance_M_Sword_Tidesorrow'),
    ("SmithCharade", '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_Reward'),
    ("Minstrel", '/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Minstrel/Balance/Balance_M_Blunt_Minstrel'),
    ("GoblinsBane", '/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/GoblinsBane/Balance/Balance_M_Sword_GoblinsBane'),
    ("Tidesorrow_leg", '/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow_leg/Balance/Balance_M_Sword_Tidesorrow_Leg'),
]:
    melee_balances.append((
        cname,
        '',
        'Named Melee Weapon',
        cobj,
        ))
melee_balances.sort()


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
            'BODY',
            'CLASS',
            'BODY SECONDARY',
            'CLASS SECONDARY',
            'CLASS STAT',
            'CLASS STAT SECONDARY',
            'LEGENDARY AUG',
            'PASSIVE SKILL COMBO',
            'PASSIVE SKILL PARTS',
            'PLAYER STAT',
            'RARITY',
            ]),
        ('amulet_balances.csv', 'amulet_balances_long.csv', amu_balances, 'Name', None, [
            'BODY',
            'CLASS STAT',
            'ELEMENT',
            'MINOR STAT',
            'RARITY',
            ]),
        ('melee_balances.csv', 'melee_balances_long.csv', melee_balances, 'Name', 'Type', None),
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
                if len(bal.raw_bal_data['Manufacturers']) > 1:
                   # Excluding reporting for the ones that I've already looked at
                   if bal_name not in {
                           '/Game/Gear/GrenadeMods/_Design/_Unique/Chupa/Balance/InvBalD_GM_Chupa',
                           '/Game/Gear/GrenadeMods/_Design/_Unique/FireStorm/Balance/InvBalD_GM_VLA_FireStorm',
                           '/Game/Gear/GrenadeMods/_Design/_Unique/Quasar/Balance/InvBalD_GM_Quasar',
                           '/Game/Gear/GrenadeMods/_Design/_Unique/StormFront/Balance/InvBalD_GM_StormFront',
                           '/Game/Gear/GrenadeMods/_Design/_Unique/TranFusion/Balance/InvBalD_GM_TranFusion',
                           '/Game/Gear/GrenadeMods/_Design/_Unique/WidowMaker/Balance/InvBalD_GM_WidowMaker',
                           }:
                       print('WARNING: {} has {} manufacturers'.format(bal_name, len(bal.raw_bal_data['Manufacturers'])))

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

                    # Figure out what the main label should be for this part type
                    if bal_name == "/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Balance/Balance_Amulet_Unique_BlazeOfGlory":
                        print("ok")
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

