import json, math, sys
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
SOV = {'JPN','KOR','PRK','IND','NPL','BGD','LKA','PAK','TUR','MNG','IRN','MMR','AFG','TJK','UZB','KAZ','KGZ','TKM','AZE','BTN','ETH','ERI','SOM','DJI'}
LON0, LON1, LAT0, LAT1 = 25, 150, -11, 56
W, H = 1000, 760
def merc(lat): return math.log(math.tan(math.pi/4 + math.radians(lat)/2))
Y0, Y1 = merc(LAT0), merc(LAT1)
def P(lon, lat):
    x = (lon - LON0) / (LON1 - LON0) * W
    y = (Y1 - merc(max(min(lat, 80), -80))) / (Y1 - Y0) * H
    return x, y
paths = []
labels = {}
for f in d['features']:
    p = f['properties']; iso = p.get('ADM0_A3') or p.get('ISO_A3')
    g = f['geometry']
    polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    dstr = []
    xs = []; ys = []
    for poly in polys:
        for ring in poly:
            if not any(LON0-15 < x < LON1+15 and LAT0-10 < y < LAT1+15 for x, y in ring): continue
            pts = [P(x, y) for x, y in ring[::1]]
            dstr.append('M' + 'L'.join(f'{a:.1f},{b:.1f}' for a, b in pts) + 'Z')
            xs += [a for a, b in pts]; ys += [b for a, b in pts]
    if not dstr: continue
    sov = iso in SOV
    paths.append(f'<path d="{"".join(dstr)}" class="{"sov" if sov else "oth"}" data-iso="{iso}"/>')
for iso, (lon, lat) in {'JPN': (138.5, 37), 'KOR': (127.8, 36.3), 'IND': (79, 22), 'TUR': (35, 39), 'MNG': (103, 46.5), 'CHN': (104, 33), 'RUS': (100, 60), 'IRN': (54, 32.5)}.items():
    labels[iso] = [round(v, 1) for v in P(lon, lat)]
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><style>.sov{{fill:#D9572B;stroke:#2B2118;stroke-width:1.2;stroke-linejoin:round}}.oth{{fill:#D8CBAA;stroke:#8C7C5E;stroke-width:.8;stroke-linejoin:round}}</style>' + ''.join(paths) + '</svg>'
open(out, 'w').write(svg)
json.dump({'W': W, 'H': H, 'labels': labels}, open(out + '.json', 'w'))
print(len(paths), labels)
