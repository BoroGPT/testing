import json
import argparse
from pathlib import Path


def load_cards(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_cards(cards):
    for card in cards:
        print(f"{card['name']} - {card['type']} - {card['mana_cost']}")


def search_cards(cards, query):
    query_lower = query.lower()
    return [c for c in cards if query_lower in c['name'].lower()]


def main():
    parser = argparse.ArgumentParser(description='Magic the Gathering Codex')
    parser.add_argument('action', choices=['list', 'search'])
    parser.add_argument('query', nargs='?', help='Name to search for')
    parser.add_argument('--data', default=Path(__file__).with_name('cards.json'))
    args = parser.parse_args()

    cards = load_cards(args.data)

    if args.action == 'list':
        list_cards(cards)
    elif args.action == 'search':
        if not args.query:
            parser.error('search requires a query string')
        matches = search_cards(cards, args.query)
        if matches:
            for card in matches:
                print(json.dumps(card, indent=2))
        else:
            print('No matches found')


if __name__ == '__main__':
    main()
