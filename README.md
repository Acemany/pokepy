# pokepy
A Python script to show pokemon sprites in the terminal.

![pokeshell4](https://user-images.githubusercontent.com/17132214/157562228-6ee73b46-9287-45de-823b-e7c43001b00e.gif)

Key features include:

| ✔️ animated sprites | ✔️ multiple pokemon | ✔️ multilingual | ✔️ terminal fit | ✔️ tab completions |
|:-:|:-:|:-:|:-:|:-:|

## Dependencies

| - [bash](https://www.gnu.org/software/bash/) | - [curl](https://curl.se/) | - [jq](https://stedolan.github.io/jq/) | - [imagemagick](https://imagemagick.org/) | - [timg](https://github.com/hzeller/timg)/[chafa](https://github.com/hpjansson/chafa/) |
|:-:|:-:|:-:|:-:|:-:|

## Installation

You can install/uninstall pokepy using [`just`](https://github.com/casey/just).

By default the install directory is `/usr/local/`, which will allow you to run `pokepy`
anywhere on your system as well as add shell completions.

You can also specify the install directory, but you'll have to make sure that directory is on your `$PATH`
if you want to run `pokepy` from anywhere.

```bash
# install
just install [<install_dir>]

# uninstall
just uninstall [<install_dir>]
```

If you don't have `just` or don't want to use it, you can directly use the `install.sh` and `uninstall.sh` scripts.

```bash
# install
./install.sh [install_dir]

# uninstall
./uninstall.sh [install_dir]
```

Remember to prepend the install/uninstall command with `sudo` if you need to.

If you do not want to install then you can still run pokepy anywhere
by adding the following lines to your `~/.bashrc`.

```bash
export PATH=/path/to/pokepy:$PATH
```

## Usage

```bash
pokepy --help
```

or if running from this directory:
```bash
./bin/pokepy --help
```

## Examples
![pokeshell1](https://user-images.githubusercontent.com/17132214/157558398-580213fa-3f46-4332-a24e-71bab1c4d033.png)
![pokeshell2](https://user-images.githubusercontent.com/17132214/157558403-8b83eb3d-4e54-44af-b05e-e3cb9a0d1ab3.png)
![pokeshell3](https://user-images.githubusercontent.com/17132214/157558404-ca22357f-7d21-41b4-9cad-282c863205f5.png)

## Integration

### hyfetch
[hyfetch](https://github.com/hykilpikonna/hyfetch) is an active fork of
[neofetch](https://github.com/dylanaraps/neofetch). Most importantly, it
has fixes for properly displaying ascii. The updated `neofetch` can be run
with the [`neowofetch`](https://github.com/hykilpikonna/hyfetch#running-updated-original-neofetch)
command and uses your existing `neofetch` config.

To use `pokepy` with `hyfetch` add the following to your `neofetch`
config file: `~/.config/neofetch/config`:
```
image_backend="ascii"
image_source=$(POKEPY_COMMAND)
```
where `POKEPY_COMMAND` is what you would run in the terminal.

For example, including the below in your `neofetch` config file
```
image_backend="ascii"
image_source=$(pokepy politoed)
```
and running `neowofetch` gives the following:

![hyfetch-integration](https://user-images.githubusercontent.com/17132214/188514218-60248920-8361-4bc6-93cd-75accfafa04f.png)

## Sources
A great amount of gratitude goes to the following projects, without which
`pokepy` would not be possible. Please star/support these sources!

Small sprites: [msikma/pokesprite](https://github.com/msikma/pokesprite)

Big sprites and localization: [PokeAPI](https://pokeapi.co/)
- Specifically: [PokeAPI/pokeapi](https://github.com/PokeAPI/pokeapi) and [PokeAPI/sprites](https://github.com/PokeAPI/sprites)

Animated sprites: [ProjectPokemon](https://projectpokemon.org/home/docs/spriteindex_148)

## Similar Projects
pokepy is a fork of a pokeshell, and pokeshell is not the first player in the pokemon shell art niche and nor will it
be the last. (I just hope that the next project can take these ideas and only
expand on them.) Below is a feature list of some projects (
[acxz/pokescript](https://github.com/acxz/pokescript),
[phoneybadger/pokemon-colorscripts](https://gitlab.com/phoneybadger/pokemon-colorscripts),
[talwat/pokeget-rs](https://github.com/talwat/pokeget-rs))
that also fill this role and what makes `pokepy`/`pokeshell` unique among them.

| **Feature**                  | **pokeshell** | **pokescript** | **colorscripts** | **pokeget-rs** |
|:----------------------------:|:-------------:|:--------------:|:----------------:|:--------------:|
| random                       | ✔️            | ✔️             | ✔️               | ✔️             |
| small                        | ✔️            | ✔️             | ✔️               | ✔️             |
| big                          | ✔️            | ❌             | ❌               | ❌             |
| animated                     | ✔️            | ❌             | ❌               | ❌             |
| terminal fit                 | ✔️            | ❌             | ❌               | ❌             |
| multilingual                 | ✔️            | ✔️             | ❌               | ❌             |
| genders                      | ✔️            | ✔️             | ❌               | ❌             |
| tab completion               | ✔️            | ✔️             | ❌               | ❌             |
| multiple pokemon             | ✔️            | ✔️             | ❌               | ✔️             |
| no internet                  | ❌            | ✔️             | ✔️               | ✔️             |
| block size <sup>#</sup>      | ANSI          | half           | half             | half           |
| # dependencies <sup>-</sup>  | 5             | 1              | 1                | 0              |
| cached speed <sup>+</sup>    | 1x (76.9 ms)  | 11x (7.1 ms)   | 2x (37.5 ms)     | 37x  (2.1 ms)  |
| first run speed <sup>+</sup> | 1x (241.2 ms) | 34x (7.1 ms)   | 6x (37.5 ms)     | 115x (2.1 ms)  |

<sup>#</sup>: in order of resolution: ANSI > half

<sup>-</sup>: pokepy/colorscripts uses python, pokeshell/pokescript uses bash, pokeget-rs uses rust

<sup>+</sup>: Normalized to pokeshell, tested with [hyperfine](https://github.com/sharkdp/hyperfine), larger
is faster

### Other Similar Projects
- [aflaaq/pokemon-icat](https://github.com/aflaaq/pokemon-icat)
    Show Pokemon sprites in Kitty
- [eramdam/pokemonshow](https://github.com/eramdam/pokemonshow)
    Show Pokemon sprites using JavaScript

## Other Pokémon Sprite Terminal Projects
- [rmccorm4/Pokefetch](https://github.com/rmccorm4/pokefetch)
    Fetch Pokedex entries in your terminal
- [HRKings/pokemonsay-newgenerations](https://github.com/HRKings/pokemonsay-newgenerations)
    Cowsay for Pokemon
- [31marcobarbosa/pokeTerm](https://github.com/31marcobarbosa/pokeTerm)
    Display random Pokemon sprite upon opening a terminal
