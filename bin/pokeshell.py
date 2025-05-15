#!/usr/bin/env python3

from argparse import Namespace, ArgumentParser
from random import choice, randint
from sys import exit as _exit
from pathlib import Path
from json import load
from os import system

from signal import signal, SIGPIPE, SIG_DFL
from requests import get

signal(SIGPIPE, SIG_DFL)
MY_DIR = Path(__file__).parent.resolve()


class Pokeshell(Namespace):
    small: bool
    animated: bool
    big: bool
    show_name: bool
    filename: bool
    remove_cache: bool
    help: bool
    pokemons: list[str]


def stat(url: str):
    return get(url, timeout=50).status_code


def get_json(url: str):
    return get(url, timeout=50).json()


def get_pic(url: str, path: str | Path):
    with open(path, 'wb') as f:
        f.write(get(url, timeout=50).content)


def _help():
    print('pokeshell: Show Pokemon sprites in the terminal\n\n'

          'Usage: pokeshell [OPTION] POKEMON...')
    for i, j in (("-b, --big", "Display big sprites (default)"),
                 ("-a, --animation", "Display animated sprites"),
                 ("-s, --small", "Display small sprites"),
                 ("-n, --show-name", "Show names of displayed Pokemon"),
                 ("-f, --filename", "Return only file path"),
                 ("-r, --remove-cache", "Remove cache directory"),
                 ("-h, --help", "Print this help")):
        print(f"  {i:<20}\t{j:<50}")
    print('\n'
          'Shiny: prepend "✨/s(hiny):" or "ns/not-shiny:"\n'
          '               or "all:" to POKEMON\n'
          '       prepending nothing uses the base shiny rate of 1/4096\n'
          '       prepending "all:" specifies shiny and not shiny\n\n'

          'Gender: append "+♂/m(ale)" or "+♀/f(emale)"\n'
          '               or "+all" to POKEMON\n'
          '        appending nothing uses the gender ratio of pokemon\n'
          '        appending "+all" specifies both male and female\n\n'

          'Random: use "random{,GEN,...}" for POKEMON\n'
          'can add comma separated list for random pokemon from specified gens\n'
          'note: specifying a gender for random is a suggestion as\n'
          'random pokemon may have gender restrictions\n\n'

          'Examples: pokeshell pikachu\n'
          '          pokeshell s:pikachu+♂ ns:pikachu+♀\n'
          '          pokeshell all:pikachu+all\n'
          '          pokeshell -s random s:pikachu-gmax\n'
          '          pokeshell -b charizard-mega-x+male ✨:ho-oh moltres-galar\n'
          '          pokeshell -a -n all:bulbasaur pikachu+all\n'
          '          pokeshell -n random,1,3+f s:random,4,1\n'
          '          pokeshell bulbasaur BULBASAUR 1 フシギダネ fushigidane\n'
          '          pokeshell s:이상해씨 妙蛙種子+♀ Bulbizarre Bisasam\n'
          '          pokeshell -f nidoran-f+f nidoran-m type-null farfetchd sirfetchd')


def main():
    parser = ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument('-b', '--big', action='store_true')
    parser.add_argument('-a', '--animated', action='store_true')
    parser.add_argument('-s', '--small', action='store_true')
    parser.add_argument_group()
    parser.add_argument('-n', '--show-name', action='store_true')
    parser.add_argument('-f', '--filename', action='store_true')
    parser.add_argument('-r', '--remove-cache', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('pokemons', nargs='*', type=str)

    args = parser.parse_args(namespace=Pokeshell())

    # if len(args) == 1:
    #     _help()  # display help if no arguments are given
    #     _exit()

    cache_dir = Path.home()/".cache/pokeshell"
    true_gender = False

    # First flag
    if args.help:
        _help()
        _exit()
    elif args.remove_cache:
        # rm -r -v cache_dir | grep -v "removed '"
        _exit()

    # Check if any pokemon listed
    # minor fixme: ||/or the below two if statements
    if not args.pokemons:
        _help()
        print('\nYou forgot to mention any Pokemon! See help.')
        _exit()

    # Parse description
    images = list[str]()
    descriptions = args.pokemons
    for desc in descriptions:
        # Parse for shiny
        desc_arr = desc.split(':')
        if len(desc_arr) == 1:
            pokemon = desc_arr[0]
            shiny_str = ''
        else:
            shiny_str = desc_arr[0]
            pokemon = desc_arr[1]

        # Parse for gender
        desc_arr = pokemon.split('+')
        if len(desc_arr) == 1:
            pokemon = desc_arr[0]
            gender_str = ''
        else:
            pokemon = desc_arr[0]
            gender_str = desc_arr[1]

        # Parse for random
        # Delimit pokemon on comma to see if we are using random gens
        is_random = 0
        pokemon_random_arr = pokemon.split(',')
        pokemon = pokemon_random_arr[0]

        if pokemon == "random":
            is_random = 1
            gen_ids = (1, 152, 251, 387, 494, 650, 722, 810, 898)
            gen_start = 0
            gen_end = 8

            # Delimit pokemon on comma to see if we are using random gens
            if len(pokemon_random_arr) != 1:
                gens = list[int]()
                for _idx in range(1, len(pokemon_random_arr)):
                    gens.append(int(pokemon_random_arr[_idx]))

                # Pick random gen
                random_gen = choice(gens)
                gen_end = random_gen
                gen_start = gen_end-1

            # Choose random pokemon id
            pokemon_id = randint(gen_ids[gen_start], gen_ids[gen_end])
            pokemon = get_json(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')["species"]["name"]

            # TODO
            # Check to see if the pokemon has forms and if so random off that
            # upstream issue, pokeapi should list forms on pokemon_species
            # POST

            # But wait there is more
            # If random let's figure out which form to use
            # TODO

        # Get canonical name from input name
        pokemon = pokemon.lower()

        # Check if pokemon is a known identifier (id, canonical name, localized name)
        with open(MY_DIR/'../share/pokemon_identifiers.json', 'r', encoding='utf-8') as f:
            pokemon = load(f).get(pokemon, pokemon)
        # If identifier not found in our list, fall back to each backend's list

        # meowstic is weird in pokeapi (upstream issue?)
        # male shiny is actually female shiny?
        if pokemon == "meowstic":
            pokemon = "meowstic-male"

        gender_rate = 4
        if true_gender:
            is_form = False
            # Check if pokemon exists! If not use unown-? lol
            if stat(f'https://pokeapi.co/api/v2/pokemon/{pokemon}') == 404:
                # Could be a pokemon form
                # Note forms are generally inconsistant in terms of if default
                # pokemon species displays a form or doesn't.
                # See shellos vs unown for example
                is_form = True
                if stat(f'https://pokeapi.co/api/v2/pokemon-form/{pokemon}') == 404:
                    # Okay now it probably doesn't exist
                    print(f'{pokemon} is unown ?')
                    pokemon = 'unown-question'

                # FIXME giratina is weird as well between pokeapi and pokesprite
                # and probably other forms as well

            if is_form:
                pokemon_species = get_json(f'https://pokeapi.co/api/v2/pokemon-form/{pokemon}')["pokemon"]["name"]
            else:
                pokemon_species = get_json(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')["species"]["name"]

            # Ensure proper gender is used (if a pokemon cannot be male or cannot
            # be female that is enforced)
            gender_rate = get_json(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_species}')["gender_rate"]

        # meowstic is weird in pokeapi (upstream issue?)
        # convert meowstic-male back to meowstic for the other backends
        if pokemon == "meowstic-male":
            pokemon = "meowstic"
            gender_rate = 4

        if not shiny_str:
            # Random shiny chance
            shiny_str = "not-shiny"
            shiny_rate = 4096
            shiny_chance = randint(1, shiny_rate)
            if shiny_chance == shiny_rate:
                shiny_str = "shiny"

        if shiny_str == "shiny" or shiny_str == "s" or shiny_str == "✨":
            _type = "shiny"
        elif shiny_str == "not-shiny" or shiny_str == "ns":
            _type = "not-shiny"
        elif shiny_str == "all":
            # After expanding all shiny options for this pokemon, continue to next iteration
            not_shiny_desc = f"not-shiny:{pokemon}+{gender_str}"
            shiny_desc = f"shiny:{pokemon}+{gender_str}"
            descriptions = (not_shiny_desc, shiny_desc, *descriptions)
            continue
        else:
            _help()
            print('\nIncorrect shiny specifier! See help.')
            _exit()

        if not gender_str:
            # Random gender chance based on pokemon gender ratio
            if gender_rate == "-1":
                gender_str = "genderless"
            else:
                gender_div = 8
                gender_chance = randint(1, gender_div)
                if gender_chance <= gender_rate:
                    gender_str = "female"
                else:
                    gender_str = "male"

        if gender_str == "male" or gender_str == "m" or gender_str == "♂":
            if gender_rate == "8":
                if is_random == 0:
                    print(f'{pokemon} must be female!\n')
                    _exit()
                else:
                    gender = "female"
            elif gender_rate == "-1":
                if is_random == 0:
                    print(f'{pokemon} has no gender!\n')
                    _exit()
                else:
                    gender = "male"
            else:
                gender = "male"
        elif gender_str == "female" or gender_str == "f" or gender_str == "♀":
            if gender_rate == "0":
                if is_random == 0:
                    print(f'{pokemon} must be male!\n')
                    _exit()
                else:
                    gender = "male"
            elif gender_rate == "-1":
                if is_random == 0:
                    print(f'{pokemon} has no gender!\n')
                    _exit()
                else:
                    # use default gender of male
                    gender = "male"
            else:
                gender = "female"
        elif gender_str == "genderless":
            if gender_rate != "-1":
                print(f'{pokemon_species} cannot be genderless!\n')  # type: ignore
                _exit()
            else:
                # use default gender of male
                gender = "male"
        elif gender_str == "all":
            # After expanding all gender options for this pokemon, continue to next iteration
            if gender_rate == "0":
                desc = f"{shiny_str}:{pokemon}+male"
                descriptions = (desc, *descriptions)
            elif gender_rate == "8":
                desc = f"{shiny_str}:{pokemon}+female"
                descriptions = (desc, *descriptions)
            elif gender_rate == "-1":
                desc = f"{shiny_str}:{pokemon}"
                descriptions = (desc, *descriptions)
            else:
                desc_male = f"{shiny_str}:{pokemon}+male"
                desc_female = f"{shiny_str}:{pokemon}+female"
                descriptions = (desc_male, desc_female, *descriptions)
            continue
        else:
            _help()
            print('\nIncorrect gender specifier! See help.')
            _exit()

        # Create full pokemon description for filename/caching
        cache_dir.mkdir(parents=True, exist_ok=True)
        desc_full = f"{_type}:{pokemon}+{gender}"
        if args.show_name:
            # TODO: show name in various languages, potentially with a
            # -n = ja, --show-name = es, --show-name = japanese, etc.
            print(f'{desc_full}{"" if gender_str == "genderless" else "♂♀"[gender == "male"]}')

        # Check if image is cached
        is_cached = False
        possible_cached_pokemon =\
            f"{cache_dir}/{desc_full}-small.png" if args.small else\
            f"{cache_dir}/{desc_full}.gif" if args.animated else\
            f"{cache_dir}/{desc_full}-big.png"

        if Path(possible_cached_pokemon).is_file():
            is_cached = True
            image = possible_cached_pokemon

        if args.small and not is_cached:
            # default type of small sprites is "regular"
            if _type == "not-shiny":
                _type = "regular"
            if gender == "male" or pokemon == "nidoran-f":
                gender = ""

            # Only limited number is exclusively female,
            # thus need to do a check to see if female exists
            # if not revert to male (i.e. gender='')
            if stat(f'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/{_type}/{gender}/{pokemon}.png'
                    ) == 404:
                gender = ""

            image = f"{cache_dir}/{desc_full}-small.png"
            get_pic(f'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/{_type}/{gender}/{pokemon}.png',
                    image)
        elif args.animated and not is_cached:
            # default type of ani sprites is "normal"
            if _type == "not-shiny":
                _type = "normal"

            if gender == "female" and pokemon != "nidoran-f":
                gender = "-f"
            else:
                gender = ""

            # Only limited number is exclusively female,
            # thus need to do a check to see if female exists
            # if not revert to male (i.e. gender='')
            if stat(f'https://projectpokemon.org/images/{_type}-sprite/{pokemon}{gender}.gif') == 404:
                gender = ""

            # ani sprites unique naming search and replace
            # nidoran-f/m => nidoran_f/m
            pokemon = pokemon.replace('nidoran-f', 'nidoran_f')
            pokemon = pokemon.replace('nidoran-m', 'nidoran_m')
            # type-null => typenull
            pokemon = pokemon.replace('type-null', 'typenull')
            # mega-{x/y} => mega{x/y}
            pokemon = pokemon.replace('mega-', 'mega')
            # gmax => gigantamax
            pokemon = pokemon.replace('gmax', 'gigantamax')

            image = f"{cache_dir}/{desc_full}.gif"
            get_pic(f'https://projectpokemon.org/images/{_type}-sprite/{pokemon}{gender}.gif',
                    image)
        elif not is_cached:
            # default type of big sprites is "default"
            _fallback = "default"
            if _type == "not-shiny" and gender != "female":
                _desc = "default"
            elif _type == "not-shiny" and gender == "female":
                _desc = "female"
                _fallback = "default"
            elif _type == "shiny" and gender != "female":
                _desc = "shiny"
            else:
                _desc = "shiny_female"
                _fallback = "shiny"

            # meowstic is weird in pokeapi (upstream issue?)
            # male shiny is actually female shiny?
            if pokemon == "meowstic":
                pokemon = "meowstic-male"

            pic_url = get_json(f'https://pokeapi.co/api/v2/pokemon-form/{pokemon}')["sprites"].get(f"front_{_desc}", None)

            if pic_url is None:
                pic_url = get_json(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')["sprites"].get(f"front_{_desc}", None)
                if not pic_url:
                    pic_url = None

            # Only limited number is exclusively female,
            # thus need to do a check to see if female exists
            # if not revert to male (i.e. gender='')
            # note for female only pokemon, pokeapi uses male classifier
            if pic_url is None:
                _desc = _fallback  # type: ignore
                pic_url = get_json(f'https://pokeapi.co/api/v2/pokemon-form/{pokemon}')["sprites"].get(f"front_{_desc}", None)
                if pic_url is None:
                    pic_url = get_json(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')["sprites"].get(f"front_{_desc}", None)
            image = f"{cache_dir}/{desc_full}-big.png"
            get_pic(pic_url, image)
        images.append(image)  # type: ignore

    if args.filename:
        print(' '.join(images))
        return

    scale = 0
    trim = 1
    pixel_perfect = 1
    cache = 1

    qweqweqwe =\
        f"source {MY_DIR/'imageshell/imageshell'}\n"\
        f"images=({' '.join((f'\"{i}\"' for i in images))})\n"\
        f"imgshl_display images {int(args.animated)} {scale} {trim} {pixel_perfect} {cache} \"{cache_dir}\""

    system(qweqweqwe)


if __name__ == "__main__":
    main()
