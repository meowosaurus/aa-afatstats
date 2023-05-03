# A(nother) FAT Statistics
An alliance auth plugin that extends ppfeufer's aFAT plugin with more statistics and a leaderboard. aFAT does have statistics, but they are limited, as it only shows statistics for every single character. AFATstats shows FATs for different roles in fleet and not per character, but per player. 

# Warning
This plugin is not production ready.

# Current Features
* Capsuleer leaderboard
  * Top Logi
  * Top Boosts
  * Top Tackle
  * Top Snowflakes 
  * Top Caps
  * Top FAX
  * Top Supers
  * Top Titans
* Corporations leaderboard
  * Absolute Participation (all fats for the current month)
  * Relative Participation (all fats relative to their size)
  * Logi Participation
  * Boosts Participation
  * Tackle Participation
  * Snowflakes Participation
  * Caps Participation
  * FAX Participation
  * Supers Participation
  * Titans Participation
* Permissions for every statistic

## Planned
* Corporations leaderboard
  * Shit metric (Admin selects the min. FATs per month and it calculates how bad a corporation is relative to their size)
* Alliance statistics
  * FAT increase / decrease compared to other months
  * Logi FAT increase / decrease
  * Boosts FAT increase / decrease
  * Tackle FAT increase / decrease
  * Snowflake FAT increase / decrease
  * Caps FAT increase / decrease
  * FAX FAT increase / decrease
  * Supers FAT increase / decrease
  * Titans FAT increase / decrease
* Automated updates every x minutes
* Introducing graphs
* Search

### Active devs:
* [Meowosaurus](https://github.com/meowosaurus)

# Installation

## Alliance Auth Production
WARNING: THIS PLUGIN IS NOT PRODUCTION READY!

1.) Install the pip package via `pip install git+https://github.com/meowosaurus/aa-afatstats`

2.) Add `afatstat` to your `INSTALLED_APPS` in your projects `local.py`

3.) Add the following celery task to your `local.py`

```python
# afatstats - https://github.com/meowosaurus/aa-afatstats
CELERYBEAT_SCHEDULE['afatstats_recalculate_data'] = {
    'task': 'afatstats.tasks.recalculate_data',
    'schedule': crontab(minute="*/1", hour="0"),
}
```

4.) Migrate, then restart your server

## Alliance Auth Development 
Make sure you have installed alliance auth in the correct way: https://allianceauth.readthedocs.io/en/latest/development/dev_setup/index.html

1.) Download the repo `git clone https://github.com/meowosaurus/aa-afatstats`

2.) Make sure it's under the root folder `aa-dev`, not under `myauth` 

3.) Change directory into `aa-dev` aand run `pip install -e aa-afatstats`

4.) Add `afatstat` to your `INSTALLED_APPS` in your projects `local.py`

5.) Add the following celery task to your `local.py`

```python
# afatstats - https://github.com/meowosaurus/aa-afatstats
CELERYBEAT_SCHEDULE['afatstats_recalculate_data'] = {
    'task': 'afatstats.tasks.recalculate_data',
    'schedule': crontab(minute="*/1", hour="0"),
}
```

6.) Change directory into `myauth`

7.) Make migrations with `python manage.py makemigrations`

8.) Migrate with `python manage.py migrate`

9.) Restart auth with `python manage.py runserver`

## Permissions
Perm | Admin Site | Auth Site 
 --- | --- | --- 
basic_access | None | Can view this app
capsuleer_top | None | Can access capsuleer top statistics
capsuleer_logi | None | Can access capsuleer logi statistics
capsuleer_boosts | None | Can access capsuleer boosts statistics
capsuleer_tackle | None | Can access capsuleer tackle statistics
capsuleer_snowflakes | None | Can access capsuleer snowflakes statistics
capsuleer_caps | None | Can access capsuleer caps statistics
capsuleer_fax | None | Can access capsuleer fax statistics
capsuleer_supers | None | Can access capsuleer supers statistics
capsuleer_titans | None | Can access capsuleer titans statistics
corporations_total | None | Can access corporation total statistics
corporations_relative | None | Can access corporation relative statistics
corporations_logi | None | Can access corporation logi statistics
corporations_boosts | None | Can access corporation boosts statistics
corporations_tackle | None | Can access corporation tackle statistics
corporations_snowflakes | None | Can access corporation snowflakes statistics
corporations_caps | None | Can access corporation caps statistics
corporations_fax | None | Can access corporation fax statistics
corporations_supers | None | Can access corporation supers statistics
corporations_titans | None | Can access corporation titans statistics
