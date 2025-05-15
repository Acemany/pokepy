#!/usr/bin/env python
# /// script
# dependencies = [
#     "aiohttp",
# ]
# ///

# Script to create a mapping between various identifiers for the same pokemon

from asyncio import run, gather
from itertools import batched
from json import loads, dump
from pathlib import Path
from typing import Any

from aiohttp import ClientSession


print('Obtaining pokemon identifiers...')


async def get(url: str, session: ClientSession) -> dict[str, Any]:
    async with session.get(url=url) as response:
        return loads(await response.read())


async def get_names(url: str, session: ClientSession, n: int):
    out: dict[str, Any] = {}

    pokemon = await get(url, session)
    pokemon_name = pokemon['name']  # Canonical name

    # "\033[F\033[K" moves to the start of the line, up, and clears the line
    print(f'\033[F\033[K{n}: {pokemon_name}')

    out |= {pokemon['id']: pokemon_name,
            pokemon_name: pokemon_name}

    # Localized names
    out |= {name['name'].casefold(): pokemon_name
            for name in pokemon['names']}

    return out


async def main():
    step = 25

    pokemons_dict: dict[str, str] = {}
    async with ClientSession() as session:
        pokemons_count = (await get('https://pokeapi.co/api/v2/pokemon-species', session))['count']
        pokemons: list[dict[str, Any]] = (await get(f'https://pokeapi.co/api/v2/pokemon-species?limit={pokemons_count}',
                                                    session))['results']

        for i, batch in enumerate(batched(pokemons, step)):
            for k in await gather(*(get_names(url['url'], session, i*step+j)
                                    for j, url in enumerate(batch))):
                pokemons_dict |= k
    print(f'Finalized all. Return is a list of len {len(pokemons)} outputs.')

    # TODO get localized form names: once done add to readme
    # Example response: https://pokeapi.co/api/v2/pokemon-form/arceus-fairy
    # Resources: https://github.com/PokeAPI/pokeapi/blob/f3fd16c59edf9defab8be3c24f43cd768747199b/data/v2/csv/pokemon_form_names.csv
    # The only place where complete form names are localized: https://www.pokeos.com/pokedex/585-autumn
    # For forms may have to massage them ourselves i.e. <japanese-pokemon-name>-<japanese-form-name>
    # where the arguments can be requested from the endpoints,
    # but being careful that the translated word of "form" doesn't show up
    # i.e. canonical name: deerling-autumn, jp name: シキジカ-はる (i.e. deerling-autumn) instead of "シキジカ-はるのすがた" (i.e. deerling-autumnform
    pokemons_dict |= {"シキジカ-あき": "deerling-autumn"}

    return pokemons_dict


print('\nObtained pokemon identifiers.')

with open(Path(__file__).parent.parent/'share/pokemon_identifiers.json',
          'w', encoding='utf-8') as f:
    dump(run(main()), f, ensure_ascii=False)
