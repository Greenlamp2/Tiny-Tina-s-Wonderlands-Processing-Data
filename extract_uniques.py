import io
import json
import lzma
import re

import pkg_resources

if __name__ == "__main__":
    gears = ["Weapons", "Shields", "Pauldrons", "Amulets", "Melee", "Rings", "SpellMods"]
    # gears = ["Amulets",]
    check = {}
    extract = {}
    for gear in gears:
        extract[gear] = []
        check[gear] = []
    with lzma.open(io.BytesIO(pkg_resources.resource_string(
            __name__, 'db/inventoryserialdb.json.xz'
            ))) as df:
        db = json.load(df)
    keys = db.keys()
    for key in keys:
        data = db[key]
        assets = data["assets"]

        for asset in assets:
            if "_OakWeapons" in asset or "Maliwan" in asset:
                continue
            regexp = r'^\/(Game\/|Game\/PatchDLC\/Indigo1\/)Gear(\/_Design)?\/(?P<type>.*?)(\/.*)?\/(_Unique.?)\/(.*?\/)(Balance\/)?(Balance_|InvBalD_Shield_|PartSet_Spell_|Bal_)(?P<name>.*)\.(?P<name2>.*)$'
            pat = re.compile(regexp)
            match = pat.match(asset)
            if not match:
                continue
            match = pat.match(asset).groupdict()
            type = match["type"] if match["type"] != "Wards" else "Shields"
            name = match["name"]
            name2 = match["name2"]
            if not extract.get(type, None):
                extract[type] = []
            if not check.get(type, None):
                check[type] = []
            stripped = asset.split(".")[0]
            stripped_name = name2.split("_")[-1]
            check[type].append(stripped)
            extract[type].append([stripped_name, stripped])

    # test if everything from before is still working:

    correct = True

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
        if balance_name not in check["Weapons"]:
            print("{} is missing".format(balance_name))
            correct = False


    for (cname, cobj) in [
        ("SelectiveAmnesia", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SelectiveAmnesia/Balance/Balance_Armor_SelectiveAmnesia'),
        ("Calamity", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Calamity/Balance/Balance_Armor_Calamity'),
        ("Claw", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Claw/Balance/Balance_Armor_MantisClaw'),
        ("DiamondGauntlets", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DiamondGauntlets/Balance/Balance_Armor_DiamondGauntlets'),
        ("HeadOfTheSnake", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/HeadOfTheSnake/Balance/Balance_Armor_HeadOfTheSnake'),
        ("Pandemecium", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Pandemecium/Balance/Balance_Armor_Pandemecium'),
        ("SmartArmor", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SmartArmor/Balance/Balance_Armor_SmartArmor'),
        ("SteelGauntlets", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SteelGauntlets/Balance/Balance_Armor_SteelGauntlets'),
        ("ArmorThatSucks", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Barb'),
        ("ArmorThatSucks", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Knight'),
        ("ArmorThatSucks", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Mage'),
        ("ArmorThatSucks", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Necro'),
        ("ArmorThatSucks", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Ranger'),
        ("ArmorThatSucks", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Rogue'),
        ("CorruptedPlatemail", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/CorruptedPlatemail/Balance/Balance_Armor_CorruptedPlatemail'),
        ("DeathlessMantle", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DeathlessMantle/Balance/Balance_Armor_DeathlessMantle'),
        ("Amalgam", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Amalgam/Balance/Balance_Armor_Amalgam'),
        ("Bladesinger", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Bladesinger/Balance/Balance_Armor_Bladesinger'),
        ("BigBMittens", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/BigBMittens/Balance/Balance_Armor_BigBMittens'),
        ("Tabula", '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Tabula/Balance/Balance_Armor_Tabula'),
    ]:
        if cobj not in check["Pauldrons"]:
            print("{} is missing".format(cobj))
            correct = False

    for (cname, cobj) in [
        ("BlazeOfGlory", "/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Balance/Balance_Amulet_Unique_BlazeOfGlory"),
        ("Frenzied", "/Game/Gear/Amulets/_Shared/_Unique/Frenzied/Balance/Balance_Amulet_Unique_Frenzied"),
        ("SacSkeep", "/Game/Gear/Amulets/_Shared/_Unique/SacSkeep/Balance_Amulets_SacSkeep"),
        ("OverflowBloodbag", "/Game/Gear/Amulets/_Shared/_Unique/OverflowBloodbag/Balance_Amulets_OverflowBloodbag"),
        ("GTFO", "/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO"),
        ("RonRivote", "/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote"),
        ("JointTraining", "/Game/Gear/Amulets/_Shared/_Unique/JointTraining/Balance/Balance_Amulet_Unique_JointTraining"),
        ("Bradluck", "/Game/Gear/Amulets/_Shared/_Unique/Bradluck/Balance/Balance_Amulet_Unique_Bradluck"),
        ("UniversalSoldier", "/Game/Gear/Amulets/_Shared/_Unique/UniversalSoldier/Balance/Balance_Amulet_Unique_UniversalSoldier"),
        ("Harbinger", "/Game/Gear/Amulets/_Shared/_Unique/Harbinger/Balance/Balance_Amulet_Unique_Harbinger"),
        ("Theruge", "/Game/Gear/Amulets/_Shared/_Unique/Theruge/Balance/Balance_Amulet_Unique_Theruge"),
        ("HarmoniousDingleDangle", "/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb"),
        ("HarmoniousDingleDangle", "/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage"),
        ("HarmoniousDingleDangle", "/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC"),
        ("HarmoniousDingleDangle", "/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro"),
        ("HarmoniousDingleDangle", "/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger"),
        ("HarmoniousDingleDangle", "/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue"),
    ]:
        if cobj not in check["Amulets"]:
            print("{} is missing".format(cobj))
            correct = False

    for (cname, cobj) in [
        ("Axe_SmithCharade_MissionWeapon", "/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_MissionWeapon"),
        ("Sword_IntroMission", "/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission"),
        ("Sword_IntroMission_SkellySword", "/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission_SkellySword"),
        ("Axe_FirstMelee", "/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/FirstMelee/Balance_M_Axe_FirstMelee"),
        ("Blunt_LeChancesLastLeg", "/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/LeChancesLastLeg/Balance_M_Blunt_LeChancesLastLeg"),
        ("Sword2H_BansheeClaw", "/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/BansheeClaw/Balance_M_Sword2H_BansheeClaw"),
        ("Axe_MiningPick", "/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Balance_M_Axe_MiningPick"),
        ("Blunt_Fish", "/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Fish/Balance_M_Blunt_Fish"),
        ("Sword2H_MageStaff", "/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/MageStaff/Balance_M_Sword2H_MageStaff"),
        ("Blunt_FryingPan", "/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/FryingPan/Balance_M_Blunt_FryingPan"),
        ("Blunt_PegLeg", "/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/PegLeg/Balance_M_Blunt_PegLeg"),
        ("Sword_DiamondGuard", "/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/DiamondGuard/Balance_M_Sword_DiamondGuard"),
        ("Axe_SnakeStick", "/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SnakeStick/Balance_M_Axe_SnakeStick"),
        ("Blunt_Pincushion", "/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Pincushion/Balance_M_Blunt_Pincushion"),
        ("Sword_Ragnarok", "/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/Ragnarok/Balance_M_Sword_Ragnarok"),
        ("Sword_SpellBlade", "/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/SpellBlade/Balance_M_Sword_SpellBlade"),
        ("Sword2H_Dragonlord", "/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Dragonlord/Balance_M_Sword2H_Dragonlord"),
        ("Sword2H_PaladinSword", "/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/PaladinSword/Balance/Balance_M_Sword2H_PaladinSword"),
        ("Axe_BodySpray", "/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/BodySpray/Balance/Balance_M_Axe_BodySpray"),
        ("Sword_Tidesorrow", "/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow/Balance/Balance_M_Sword_Tidesorrow"),
        ("Axe_SmithCharade_Reward", "/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_Reward"),
        ("Blunt_Minstrel", "/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Minstrel/Balance/Balance_M_Blunt_Minstrel"),
        ("Sword2H_BansheeClaw_Leg", "/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/BansheeClaw_leg/Balance_M_Sword2H_BansheeClaw_Leg"),
        ("Sword_TwinSoul", "/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/TwinSoul/Balance_M_Sword_TwinSoul"),
        ("Sword_GoblinsBane", "/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/GoblinsBane/Balance/Balance_M_Sword_GoblinsBane"),
        ("Sword_Tidesorrow_Leg", "/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow_leg/Balance/Balance_M_Sword_Tidesorrow_Leg"),
    ]:
        if cobj not in check["Melee"]:
            print("{} is missing".format(cobj))
            correct = False


    for (cname, cobj) in [
        ("ElderWyvern", '/Game/Gear/Rings/_Shared/_Unique/ElderWyvern/Balance/Balance_Ring_ElderWyvern'),
        ("Sharklescent", '/Game/Gear/Rings/_Shared/_Unique/Sharklescent/Balance/Balance_Ring_Sharklescent'),
        ("InsightRing", '/Game/Gear/Rings/_Shared/_Unique/InsightRing/Balance/Balance_Rings_InsightRing'),
        ("DriftwoodRing", '/Game/Gear/Rings/_Shared/_Unique/DriftwoodRing/Balance_Rings_DriftwoodRing'),
        ("Cond_LowHealth", '/Game/Gear/Rings/_Shared/_Unique/Cond_LowHealth/Balance_R_LowHealth'),
        ("Cond_Dungeon", '/Game/Gear/Rings/_Shared/_Unique/Cond_Dungeon/Balance_R_Dungeon'),
        ("Cond_Boss", '/Game/Gear/Rings/_Shared/_Unique/Cond_Boss/Balance_R_Boss'),
        ("Cond_FullShield", '/Game/Gear/Rings/_Shared/_Unique/Cond_FullShield/Balance_R_FullShield'),
        ("Cond_Healthy", '/Game/Gear/Rings/_Shared/_Unique/Cond_Healthy/Balance_R_Healthy'),
        ("Cond_LowAmmo", '/Game/Gear/Rings/_Shared/_Unique/Cond_LowAmmo/Balance_R_LowAmmo'),
        ("Cond_LowShield", '/Game/Gear/Rings/_Shared/_Unique/Cond_LowShield/Balance_R_LowShield'),
        ("Cond_SkillCooldown", '/Game/Gear/Rings/_Shared/_Unique/Cond_SkillCooldown/Balance_R_SkillCooldown'),
        ("Cond_SkillReady", '/Game/Gear/Rings/_Shared/_Unique/Cond_SkillReady/Balance_R_SkillReady'),
    ]:
        if cobj not in check["Rings"]:
            print("{} is missing".format(cobj))
            correct = False


    for (cname, cobj) in [
        ("DestructionRains", '/Game/Gear/SpellMods/_Unique/_MissionUniques/DestructionRains/Balance/Balance_Spell_DestructionRains'),
        ("LavaGoodTime", '/Game/Gear/SpellMods/_Unique/_MissionUniques/LavaGoodTime/Balance/Balance_Spell_LavaGoodTime'),
        ("AncientPowers", '/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v1'),
        ("AncientPowers", '/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v2'),
        ("AncientPowers", '/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v3'),
        ("HoleyHandGrenade", '/Game/Gear/SpellMods/_Unique/_MissionUniques/HoleyHandGrenade/Balance/Balance_Spell_HoleyHandGrenade'),
        ("LittleBluePill", '/Game/Gear/SpellMods/_Unique/_MissionUniques/LittleBluePill/Balance/Balance_Spell_LittleBluePill'),
        ("JaggedToothCrew", '/Game/Gear/SpellMods/_Unique/_MissionUniques/JaggedToothCrew/Balance/Balance_Spell_JaggedTooth'),
        ("Frostburn", '/Game/Gear/SpellMods/_Unique/_MissionUniques/Frostburn/Balance/Balance_Spell_Frostburn'),
        ("TimeSkip", '/Game/Gear/SpellMods/_Unique/TimeSkip/Balance/Balance_Spell_TimeSkip'),
        ("Dazzler", '/Game/Gear/SpellMods/_Unique/Dazzler/Balance/Balance_Spell_Dazzler'),
        ("FrozenOrb", '/Game/Gear/SpellMods/_Unique/FrozenOrb/Balance/Balance_Spell_FrozenOrb'),
        ("Laserhand", '/Game/Gear/SpellMods/_Unique/Laserhand/Balance/Balance_Spell_Laserhand'),
        ("Marshmellow", '/Game/Gear/SpellMods/_Unique/Marshmellow/Balance/Balance_Spell_Marshmellow'),
        ("GelSphere", '/Game/Gear/SpellMods/_Unique/GelSphere/Balance/Balance_Spell_GelSphere'),
        ("Barrelmaker", '/Game/Gear/SpellMods/_Unique/Barrelmaker/Balance/Balance_Spell_Barrelmaker'),
        ("Buffmeister", '/Game/Gear/SpellMods/_Unique/Buffmeister/Balance/Balance_Spell_Buffmeister'),
        ("Reviver", '/Game/Gear/SpellMods/_Unique/Reviver/Balance/Balance_Spell_Reviver'),
        ("Inflammation", '/Game/Gear/SpellMods/_Unique/Inflammation/Balance/Balance_Spell_Inflammation'),
        ("GlacialCascade", '/Game/Gear/SpellMods/_Unique/GlacialCascade/Balance/Balance_Spell_GlacialCascade'),
        ("ThreadOfFate", '/Game/Gear/SpellMods/_Unique/ThreadOfFate/Balance/Balance_Spell_ThreadOfFate'),
        ("Twister", '/Game/Gear/SpellMods/_Unique/Twister/Balance/Balance_Spell_Twister'),
        ("ArcaneBolt", '/Game/Gear/SpellMods/_Unique/ArcaneBolt/Balance/Balance_Spell_ArcaneBolt'),
        ("Sawblades", '/Game/Gear/SpellMods/_Unique/Sawblades/Balance/Balance_Spell_Sawblades'),
        ("Watcher", '/Game/Gear/SpellMods/_Unique/Watcher/Balance/Balance_Spell_Watcher'),
    ]:
        if cobj not in check["SpellMods"]:
            print("{} is missing".format(cobj))
            correct = False

    if correct:
        print('Everything is okay')

    for gear, data in extract.items():
        print('\n\n=================[{}]=================\n'.format(gear))
        for elm in data:
            print('("{}", "{}"),'.format(elm[0], elm[1]))

