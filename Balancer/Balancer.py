#!/usr/bin/env python3

import SQL
import argparse
import json
import math

parser = argparse.ArgumentParser(description='Help balance loot in a party.')
parser.add_argument('--add-player', nargs=2,
                    help='Add a new player')
parser.add_argument('--list-players', action='store_true',
                    help='List off players')
parser.add_argument('--loot-template', action='store_true',
                    help='Create a loot template')
parser.add_argument('--split-loot', nargs=1,
                    help='Create a loot template')
parser.add_argument('-p','--party-fund', action='store_true',
                    help='Fund the party in loot splits')

args = parser.parse_args()
sql = SQL.SQL()

if args.add_player:
    sql.add_player(args.add_player[0],args.add_player[1])


elif args.list_players:
    players = sql.get_players()
    balances = sql.get_balances()

    for player in players:
        print(f"'{player['name']}' playing '{player['character_name']}' with {balances[player['player_id']]:,.2f} gp")


elif args.loot_template:
    template = {}
    
    template['coins'] = {}
    template['coins']['platinum'] = 0
    template['coins']['gold'] = 0
    template['coins']['silver'] = 0
    template['coins']['copper'] = 0

    template['items'] = []
    template['items'].append({"name":"sword","value":50,"amount":1, 
                               "claimed":0, "trade-good":False,})
    template['items'].append({"name":"potion","value":50,"amount":6, 
                               "claimed":0, "trade-good":False,})

    template['player_loot'] = {}
    players = sql.get_players()
    for player in players:
        template['player_loot'][player['name']] = 0

    with open("template.json",'w') as fp:
        json.dump(template,fp,indent=4)


elif args.split_loot:
    # Load the data from the given json
    with open(args.split_loot[0],'r') as fp:
        data = json.load(fp)

        # Do some sanity checking on the given JSON file
        if 'coins' not in data: raise KeyError("Coins not found in json")
        if 'platinum' not in data['coins']: raise KeyError("platinum coins not found in json")
        if 'gold' not in data['coins']: raise KeyError("gold coins not found in json")
        if 'silver' not in data['coins']: raise KeyError("silver coins not found in json")
        if 'copper' not in data['coins']: raise KeyError("copper coins not found in json")
        if 'items' not in data: raise KeyError("items not found in json")
        if 'player_loot' not in data: raise KeyError("player_loot not found in json")
        for item in data['items']:
            if 'name' not in item: raise KeyError(f"name not found in {item['name']}")
            if 'value' not in item: raise KeyError(f"value not found in {item['name']}")
            if 'amount' not in item: raise KeyError(f"amount not found in {item['name']}")
            if 'trade-good' not in item: raise KeyError(f"trade-good not found in {item['name']}")
            if 'claimed' not in item: raise KeyError(f"claimed not found in {item['name']}")
            if item['claimed'] > item['amount']: raise ValueError(f"'{item['name']}' has more claimed than exist")
        players = sql.get_players()
        for player_name in data['player_loot']:
            for db_player in players:
                if db_player['name'] == player_name: break
            else:
                raise KeyError(f"'{player_name}' isn't in the DB. Use --add-player to add them!")

    # Check claimed loot to make sure we don't have a miss match
    claimed_loot_value = 0
    for item in data['items']:
        claimed_loot_value += item['value']*item['claimed']
    for player in data['player_loot']:
        claimed_loot_value -= data['player_loot'][player]
    # Results to match with 1 gp
    if not math.isclose(claimed_loot_value, 0, rel_tol=1e-02, abs_tol=1):
        print(f"Found error in math")
        print(f"Total claimed values balanced to {claimed_loot_value:,.2f} gp, expected (nearly) zero")
        if claimed_loot_value > 0:
            print("Looks a player didn't claim loot")
        else:
            print("Looks like a player claimed loot they didn't take")
        raise ArithmeticError("Player loot and claimed loot have a mismatch")

    balances = sql.get_balances()
    party_id = sql.get_player_id('party')
    print("Initial Player Balances")
    for player_id in balances:
        print(f"{sql.get_player(player_id)['name']:>8}:{balances[player_id]:7,.2f} gp")

    total_loot_value = 0
    for item in data['items']:
        # Trade goods are sold at market value, everything else is at 50%
        if item['trade-good']:
            total_loot_value += (item['amount']-item['claimed'])*item['value']
        else:
            total_loot_value += (item['amount']-item['claimed'])*item['value']/2

    total_loot_value += data['coins']['platinum']*1e1
    total_loot_value += data['coins']['gold']*1e0
    total_loot_value += data['coins']['silver']*1e-1
    total_loot_value += data['coins']['copper']*1e-2

    remaining_loot_value = total_loot_value
    print(f"\nTotal loot to split {total_loot_value:.2f} gp.")

    # We need to keep track of the actual COINS that we split
    coin_payouts = {}
    for player_id in balances:
        coin_payouts[player_id] = 0

    # First things first, players buy their loot
    print("\nPlayer Loot Taken")
    for player in data['player_loot']:
        player_id = sql.get_player_id(player)
        print(f"{player:>8}:{data['player_loot'][player]:7,.2f} gp")
        balances[player_id] += data['player_loot'][player]

    print("\nBalance After Player Loot")
    for player_id in balances:
        print(f"{sql.get_player(player_id)['name']:>8}:{balances[player_id]:7,.2f} gp")

    party_balanced = False
    print("\nAllocate Loot until party is balanced, or loot is gone.")
    while party_balanced == False:
        print("\nLoop to equal out players.")
        # Find the lowest balance
        balances_list = list(set([balances[player_id] for player_id in balances if player_id != party_id]))
        if len(balances_list) == 1:
            print("Players are equal, split remaining loot.")
            break
        balances_list = sorted(balances_list)

        lowest_balance = balances_list[0]
        second_lowest_balance = balances_list[1]

        print(f"Lowest balance is {lowest_balance:.2f} gp")
        print(f"Target for these balances is {second_lowest_balance:.2f} gp")
        
        print("Who has this amount?")
        lowest_players = []
        for player_id in balances:
            if player_id == party_id:
                continue
            if balances[player_id] == lowest_balance:
                lowest_players.append(player_id)

        print(f"Found {len(lowest_players)} players with {lowest_balance:.2f} gp")
        for player_id in lowest_players:
            print(f"  {sql.get_player(player_id)['name']}")

        # Check to make sure we can PAY this amount!
        if remaining_loot_value < len(lowest_players) * (second_lowest_balance - lowest_balance):
            print("\nThere is not enough remaining gold to balance the groups!")
            print("Pay them what we can.")            
            for player_id in lowest_players:
                balances[player_id] += remaining_loot_value/len(lowest_players)
                coin_payouts[player_id] += remaining_loot_value/len(lowest_players)
            remaining_loot_value = 0
            break
        else: 
            print(f"Pay out {second_lowest_balance - lowest_balance:.2f} gp to each player")
            for player_id in lowest_players:
                balances[player_id] += second_lowest_balance - lowest_balance
                coin_payouts[player_id] += second_lowest_balance - lowest_balance
                remaining_loot_value -= second_lowest_balance - lowest_balance

    if remaining_loot_value > 0:    
        print(f"\nWe now have {remaining_loot_value:.2f} gp to split.")

        if not args.party_fund:
            print("Do you wish to also fund the party fund?")
            if input("(y/n)> ").lower().startswith("y"):
                args.party_fund = True

        split_number = len(balances) - 1
        if args.party_fund:
            split_number += 1

        print(f"Give each remaining member {remaining_loot_value/split_number:.2f} gp")
        for player_id in balances:
            if not args.party_fund and player_id == party_id:
                continue
            balances[player_id] += remaining_loot_value/split_number
            coin_payouts[player_id] += remaining_loot_value/split_number

    print("\nFinal Results")
    old_balances = sql.get_balances()
    transactions = {}
    for player_id in balances:
        if old_balances[player_id] != balances[player_id]:
            transactions[player_id] = balances[player_id] - old_balances[player_id]

        print(f"{sql.get_player(player_id)['name']:>8}")
        print(f"        - Old Balance: {old_balances[player_id]:7,.2f} gp")
        print(f"        - New Balance: {balances[player_id]:7,.2f} gp")
        print(f"        - Coins Paid:  {coin_payouts[player_id]:7,.2f} gp")

    print("Do you wish to commit this to the DB?")
    if input("(y/n)> ").lower().startswith("y"):
        for transaction in transactions:
            sql.add_transaction(transaction,data['name'],transactions[transaction])

else:
    parser.print_help()