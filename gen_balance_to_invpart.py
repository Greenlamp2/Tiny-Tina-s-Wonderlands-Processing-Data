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

import json
import lzma

# Creates a mapping of Balances to BPInvPart_* keys, which is used to
# find parts when doing savegame item mappings.  (The BPInvPart_*
# keys are what's used in InventorySerialNumberDatabase.dat.)
# Note that this actually generates more than just balance references,
# though we are at least ensuring that all reported objects include
# "bal" in their name.  That will likely filter out a bunch which
# don't belong, anyway.
from hotfixgenerator.bl3data import BL3Data

output_file = 'balance_to_inv_key.json.xz'
invparts = [
    "BPInvPart_SG_MAL",
    "BPInvPart_AR_DAL",
    "BPInvPart_Amulet",
    "BPInvPart_Ring",
    "BPInvPart_Shield",
    "BPInvPart_SpellMod",
    "BPInvPart_ATL_AR",
    "BPInvPart_AR_COV",
    "BPInvPart_JAK_AR",
    "BPInvPart_AR_TOR",
    "BPInvPart_VLA_AR",
    "BPInvPart_ATL_HW",
    "BPInvPart_HW_COV",
    "BPInvPart_HW_TOR",
    "BPInvPart_HW_VLA",
    "BPInvPart_PS_ATL",
    "BPInvPart_PS_COV",
    "BPInvPart_PS_DAL",
    "BPInvPart_Jakobs_Pistol",
    "BPInvPart_PS_MAL",
    "BPInvPart_Tediore_Pistol",
    "BPInvPart_PS_TOR",
    "BPInvPart_PS_VLA",
    "BPInvPart_Hyperion_Shotgun",
    "BPInvPart_SG_JAK",
    "BPInvPart_SG_TED",
    "BPInvPart_SG_Torgue",
    "BPInvPart_Dahl_SMG",
    "BPInvPart_SM_Hyperion",
    "BPInvPart_Maliwan_SMG",
    "BPInvPart_SM_TED",
    "BPInvPart_SR_DAL",
    "BPInvPart_SR_HYP",
    "BPInvPart_SR_JAK",
    "BPInvPart_MAL_SR",
    "BPInvPart_VLA_SR",
    "BPInvPart_Pauldron",
    "BPInvPart_HydraWeapon",
    "BPInvPart_Melee_Sword",
    "BPInvPart_Melee_Sword_2H",
    "BPInvPart_Melee_Axe",
    "BPInvPart_Melee_Blunt",
    "BPInvPart_Melee_Dagger",
]

mapping = {}
data = BL3Data()

for invpart in invparts:
    invpart_full = '{}_C'.format(invpart)
    print('Processing {}...'.format(invpart))
    object_names = data.get_refs_objects_by_short_name(invpart)
    if len(object_names) == 0:
        print('WARNING: {} has no result'.format(invpart))
        continue
    for object_name in object_names:
        refs = data.get_refs_to(object_name)
        for ref in refs:
            ref_full = '{}.{}'.format(
                    ref,
                    ref.split('/')[-1],
                    ).lower()
            if 'bal' not in ref_full:
                continue
            if ref_full in mapping:
                print('WARNING: {} already exists in mapping'.format(ref_full))
                continue
            mapping[ref_full] = invpart_full

with lzma.open(output_file, 'wt') as df:
    json.dump(mapping, df, separators=(',', ':'))
print('Done!  Written to {}'.format(output_file))

