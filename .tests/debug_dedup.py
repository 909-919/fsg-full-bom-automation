from fsg_bom.matcher import AssemblyMatcher
matcher = AssemblyMatcher()

# Case: Excel Data for 'sun gear'
# Excel rows usually have Assembly='Gearbox' (after remapping)
system = 'DT'
assembly = 'Gearbox'
part = 'sun gear'
key_full = matcher.canonical_key(system, assembly, part)

# Case: Scraped Data from browser.py logs
# From our previous dry-run, we saw:
# [DEBUG] Scraped Part: 'sun gear', Assembly: '', System: 'bompart' -> Key: 'BOMPART__sungear'
# Note the scraped system is 'BOMPART' because it's a raw scrape!

print(f"Excel Key: {key_full}")

# Let's inspect how browser.py scrapes the parts again
# It looks like the system label isn't being scraped correctly from the table!
