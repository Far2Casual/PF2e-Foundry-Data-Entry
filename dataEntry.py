import regex as re
from regex import sub
from pyperclip import copy
from tkinter import Tk, Frame, Canvas, Text, Button, END, BooleanVar, Menu

## As nice as it is to have these declared separately for some reason different IDEs react poorly to them being * imported.
DC = r"DD (\d+)"

ABILITY_SCORES = r"(Force|Dextérité|Constitution|Intelligence|Sagesse|Charisme)"
SAVES = r"(réflexes|volonté|vigueur|Réflexes|Volonté|Vigueur)"
SKILLS = r"(Perception|Acrobaties|Arcanes|Athlétisme|Artisanat|Duperie|Diplomatie|Intimidation|Médecine|Nature|" \
         r"Occultisme|Représentation|Religion|Société|Discrétion|Survie|Vol)"

CONDITION_COMPENDIUM = r"@UUID[Compendium.pf2e.conditionitems."

ACTIONS = ["Être furtif", "Garder l’équilibre", "Contraindre", "Ramper",
           "Faire diversion", "Démoraliser", "Désamorcer un dispositif", "Désarmer", "Gagner de l’argent", "S'échapper",
           "Feinter",
           "Force Open", "Grab an Edge", "Grapple", "High Jump", "Leap", "Liberating Step", "Long Jump",
           "Make an Impression", "Mount", "Perform", "Search", "Seek", "Sense Motive", "Shove", "Sneak",
           "Steal", "Take Cover", "Track", "Treat Disease", "Treat Poison", "Treat Wounds",
           "Trip", "Tumble Through"]

CONDITIONS = ["Aveuglée?s?", "Fatiguée?s?", "Confuse?s?", "Masquée?s?", "Éblouie?s?", "Sourde?s?", "Invisibles?",
              "Prise?s? au dépourvu", "Immobilisée?s?", "Á terre", "Inconsciente?s?", "Fascinée?s?", "Paralysée?s?",
              "Cachée?s?", "Accélérée?s?", "En fuite", "Empoignée?s?", "Entravée?s?"]

NUMBERED_CONDITIONS = ["Maladroite?s?", "Condamnée?s?", "Drainée?s?", "Affaiblie?s?", "Ralentie?s?", "Effrayée?s?",
                       "Malades?", "Étourdie?s?", "Stupefiée?s?", "Accélérée?s?"]

EQUIPMENT = []  # "Handwraps of Mighty Blows"]

FEATS = []  # "Canny Acumen", "Quick Jump"]

SPELLS = []  # "Dimension Door", "Plane Shift", "Stone Tell", "divine lance", "protection", "searing light", "divine wrath",
# "divine decree", "divine aura", "heroism", "chilling spray", "ray of frost", "cone of cold", "polar ray",
# "heal", "water walk", "electric arc", "shocking grasp", "lightning bolt", "lightning storm", "chain lightning",
# "fireball", "chilling darkness", "produce flame", "burning hands", "flaming sphere", "wall of fire", "meteor swarm",
# "magic missile", "spiritual weapon", "spirtual guardian", "spirit song", "hypercognition", "daze",
# "phantom pain", "warrior's regret", "phantasmal killer", "weird", "phantasmal calamity", "harm", "chill touch",
# "sudden blight", "enervation", "wail of the banshee", "puff of poison", "spider sting", "noxious vapors",
# "swarming wasp stings", "purple worm sting", "linnorm sting", "imp sting", "disrupt undead", "disrupting weapons",
# "breath of life", "regenerate", "true seeing", "feather fall", "jump", "mending", "illusory disguise", "charm",
# "fear", "share lore", "summon plant or fungus", "object reading", "enthrall", "bless", "mindblank", "invisibility",
# "endure elements", "knock", "earth bind", "fly", "augury"]

LOCALIZE_SAVES_ROLLS = {
    "réflexes": "reflex",
    "vigueur": "fortitude",
    "volonté": "will",
    "acrobaties": "acrobatics",
    "arcanes": "arcane",
    "athlétisme": "athletics",
    "artisanat": "crafting",
    "duperie": "deception",
    "diplomatie": "diplomacy",
    "médecine": "medecine",
    "occultisme": "occultism",
    "représentation": "performance",
    "société": "society",
    "discrétion": "stealth",
    "survie": "survival",
    "vol": "thievery"
}
LOCALIZE_PATTERN_SAVES_ROLLS = re.compile(r'\b(' + '|'.join(LOCALIZE_SAVES_ROLLS.keys()) + r')\b')

LOCALIZE_CONDITIONS = {
    "Aveuglée?s?": "XgEqL1kFApUbl5Z2",
    "Fatiguée?s?": "HL2l2VRSaQHu9lUw",
    "Confuse?s?": "yblD8fOR1J8rDwEQ",
    "Masquée?s?": "DmAIPqOBomZ7H95W",
    "Éblouie?s?": "TkIyaNPgTZFBCCuh",
    "Sourde?s?": "9PR9y0bi4JPKnHPR",
    "Invisibles?": "zJxUflt9np0q4yML",
    "Prise?s? au dépourvu": "AJh5ex99aV6VTggg",
    "Immobilisée?s?": "eIcWbB5o3pP6OIMe",
    "Á terre": "j91X7x0XSomq8d60",
    "Inconsciente?s?": "fBnFDH2MTzgFijKf",
    "Fascinée?s?": "AdPVz7rbaVSRxHFg",
    "Paralysée?s?": "6uEgoh53GbXuHpTF",
    "Cachée?s?": "iU0fEDdBp3rXpTMC",
    "Accélérée?s?": "nlCjDvLMf2EkV2dl",
    "En fuite": "sDPxOjQ9kx2RZE8D",
    "Entravée?s?": "VcDeM8A5oI6VqhbM",
    "Empoignée?s?": "kWc1fhmv9LBiTuei",
    "Maladroite?s?": "i3OJZU2nk64Df3xm",
    "Condamnée?s?": "3uh1r86TzbQvosxv",
    "Drainée?s?": "4D2KBtexWXa6oUMR",
    "Affaiblie?s?": "MIRkyAjyBeXivMa7",
    "Ralentie?s?": "xYTAsEpcJE1Ccni3",
    "Effrayée?s?": "TBSHQspnbcqxsmjL",
    "Malades?": "fesd1n5eVhpCSS18",
    "Stupefiée?s?": "e1XGnhKNSQIm5IXg",
    "Étourdie?s?": "dfCMdR4wnpbYNTix"
}
LOCALIZE_PATTERN_CONDITIONS = re.compile(r'\b(' + '|'.join(LOCALIZE_CONDITIONS.keys()) + r')\b')

LOCALIZE_TEMPLATES = {
    "émanation": "emanation",
    "explosion": "burst",
    "cône": "cone",
    "ligne": "line"
}
LOCALIZE_PATTERN_TEMPLATES = re.compile(r'\b(' + '|'.join(LOCALIZE_TEMPLATES.keys()) + r')\b')

LOCALIZE_DAMAGE = {
    "contondant": "bludgeoning",
    "contondants": "bludgeoning",
    "perforant": "piercing",
    "perforants": "piercing",
    "tranchant": "slashing",
    "tranchants": "slashing",
    "acide": "acid",
    "froid": "cold",
    "électricité": "electricity",
    "feu": "fire",
    "son": "sonic",
    "positif": "positive",
    "positifs": "positive",
    "négatif": "negative",
    "négatifs": "negative",
    "chaotique": "chaotic",
    "chaotiques": "chaotic",
    "loyal": "lawful",
    "loyaux": "lawful",
    "bon": "good",
    "bons": "good",
    "mauvais": "evil",
    "mental": "mental",
    "mentaux": "mental",
    "poison": "poison",
    "saignement": "bleed",
    "précision": "precision",
    "nécrotique": "necrotic",
    "nécrotiques": "necrotic"
}
LOCALIZE_PATTERN_DAMAGE = re.compile(r'\b(' + '|'.join(LOCALIZE_DAMAGE.keys()) + r')\b')


def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def action_sub(string, action):
    return sub(r"\b" + action + r"\b", r"@Compendium[pf2e.actionspf2e.%s]{%s}" % (action, action), string, count=1)


def condition_sub(string, condition):
    return sub(condition.lower(),
               r"%s%s]{\g<0>}" % (CONDITION_COMPENDIUM, LOCALIZE_CONDITIONS[condition]),
               string, count=1)


def condition_sub_with_stage(string, condition, stage):
    return sub(r"%s %s" % (condition.lower(), stage),
               r"%s%s]{\g<0>}" % (CONDITION_COMPENDIUM, LOCALIZE_CONDITIONS[condition]),
               string, count=1)


def equipment_sub(string, equipment):
    return sub(equipment, r"@Compendium[pf2e.equipment-srd.%s]{%s}" % (equipment, equipment), string, count=1)


def feat_sub(string, feat):
    return sub(feat, r"@Compendium[pf2e.feats-srd.%s]{%s}" % (feat, feat), string, count=1)


def spell_sub(string, spell):
    return sub(spell, r"<em>@Compendium[pf2e.spells-srd.%s]{%s}</em>" % (spell, spell), string, count=1)


def handle_actions(string):
    for action in ACTIONS:
        string = action_sub(string, action)
    return string


def handle_conditions(string):
    for condition in CONDITIONS:
        string = condition_sub(string, condition)

    # Handle this one manually due to the lack of hyphen.
    string = sub(r"pris au dépourvu", r"%sFlat-Footed]{Pris au dépourvu}" % CONDITION_COMPENDIUM, string, count=1)

    for condition in NUMBERED_CONDITIONS:
        for i in range(1, 6):
            string = condition_sub_with_stage(string, condition, i)
    return string


def handle_equipment(string):
    for equipment in EQUIPMENT:
        string = equipment_sub(string, equipment)
    return string


def handle_feats(string):
    for feat in FEATS:
        string = feat_sub(string, feat)
    return string


def handle_spells(string):
    for spell in SPELLS:
        string = spell_sub(string, spell)
    return string


def handle_activation_actions(string):
    string = sub(r"\[free-action\]", r"<span class=\"pf2-icon\">F</span>", string)
    string = sub(r"\[reaction\]", r"<span class=\"pf2-icon\">R</span>", string)
    string = sub(r"\[one-action\]", r"<span class=\"pf2-icon\">1</span>", string)
    string = sub(r"\[two-actions\]", r"<span class=\"pf2-icon\">2</span>", string)
    string = sub(r"\[three-actions\]", r"<span class=\"pf2-icon\">3</span>", string)
    return string


def handle_damage_rolls(string):
    string = sub(r" (\d)d(\d) (rounds|minutes|heures|jours)", r" [[/r \1d\2 #\3]]{\1d\2 \3}", string)
    string = sub(r"(\d+)(d\d+)?(\+\d+)? dégât(s)?( d\'éclaboussures?)?(\sde\s|\sd\'|\s)(\w*)( persistants?)?",
                 lambda x: f"[[/r {{{x.group(1)}{x.group(2) or ''}{x.group(3) or ''}}}"
                           f"[{'persistent,' if x.group(8) is not None else ''}"
                           f"{'splash,' if x.group(5) is not None else ''}"
                           f"{LOCALIZE_DAMAGE[x.group(7)] if x.group(7) in LOCALIZE_DAMAGE else ''}]]]"
                           f"{{{x.group(1)}{x.group(2) or ''}{x.group(3) or ''} dégât"
                           f"{x.group(4) if x.group(4) is not None else ''}"
                           f"{x.group(5) if x.group(5) is not None else ''}"
                           f"{x.group(6)+x.group(7) if x.group(7) in LOCALIZE_DAMAGE else ''}"
                           f"{x.group(8) or ''}}}{x.group(6)+x.group(7) if x.group(7) not in LOCALIZE_DAMAGE else ''}"
                 , string)
    string = sub(r"\[\]", "", string)
    string = sub(r"(\d+)d(\d+) (\w+)(\,|\.)", r"[[/r \1d\2 #\3]]{\1d\2 \3}\4", string)
    string = sub(r"(\d+)d(\d+)\.", r"[[/r \1d\2]]{\1d\2}.", string)
    return string


def handle_spell_heightening(string):
    string = sub(r"Intensifié \(", r"<hr />Intensifié (", string, count=1)
    string = sub(r"Intensifié \(\+(\d+)\)", r"</p><p><strong>Intensifié (+\1)</strong>", string)
    string = sub(r"Intensifié \((\d+)(\w+)\)", r"</p><p><strong>Intensifié (\1\2)</strong>", string)
    string = sub(r"<hr /></p><p><strong>Intensifié", r"</p><hr /><p><strong>Intensifié", string)
    return string


def handle_bullet_lists(string):
    # Removing bullet points, should replace with the actual bullet points.
    string = sub(r"•", "<ul><li>", string, count=1)
    string = sub(r"•", "</li><li>", string)
    return string


def handle_templates(string):
    # Add template buttons
    string = sub(r"(émanation|explosion|cône|ligne|Émanation|Explosion|Cône|Ligne) de (\d+\,?\d?) (mètres|m)",
                 r"@Template[type:\1|distance:\2]", string)
    string = sub(r"type:%s" % r"(Émanation|Explosion|Cône|Ligne)", convert_to_lower, string)
    string = sub(r"distance:(\d+\,?\d?)(]|\|)",
                 lambda x: "distance:" + str(int(float(x.group(1).replace(",", ".")) * 10 / 3)) + x.group(2), string)

    return LOCALIZE_PATTERN_TEMPLATES.sub(lambda x: LOCALIZE_TEMPLATES[x.group()], string)


def handle_third_party(string):
    # Handling for 3rd party formatting.
    string = sub(r"» (Réussite critique|Réussite|Échec|Échec critique)", r"</p><p><strong>\1</strong>", string)
    string = sub(r"»", r"•", string)
    return string


def handle_background(string):
    string = sub(r"Choose two ability boosts.", r"</p><p>Choose two ability boosts.", string)
    string = sub(r"%s" % ABILITY_SCORES, r"<strong>\1</strong>", string, count=2)
    string = sub(r"You're trained in", r"</p><p>You're trained in", string)
    string = sub(r"You gain the (.*) skill feat", r"You gain the @Compendium[pf2e.feats-srd.\1]{\1} skill feat", string)
    return string


def handle_aura(string):
    string = sub(r"<p>(\d+) feet.",
                 r"<p>@Template[type:emanation|distance:\1] @Compendium[pf2e.bestiary-ability-glossary-srd.Aura]{Aura}</p><p>",
                 string)
    return string


def companion_format(string):
    string = sub(r"Size (Tiny|Small|Medium|Large)", r"<p><strong>Size</strong> \1</p>", string)
    string = sub(r"Melee \? (\w+)(,|;) Damage (\d+)d(\d+) (\w+)",
                 r"<p><strong>Melee</strong> <span class='pf2-icon'>1</span> \1, <strong>Damage</strong> \3d\4 \5</p>",
                 string)
    string = sub(r"Melee \? (\w+) \(([^\)]+)\)(,|;) Damage (\d+)d(\d+) (\w+)",
                 r"<p><strong>Melee</strong> <span class='pf2-icon'>1</span> \1 (\2), <strong>Damage</strong> \4d\5 \6</p>",
                 string)
    string = sub(r"Str ", r"<p><strong>Str</strong> ", string)
    string = sub(r"(Dex|Con|Int|Wis|Cha) ", r"<strong>\1</strong> ", string)
    string = sub(r"Hit Points (\d+)", r"</p><p><strong>Hit Points</strong> \1</p>", string)
    string = sub(r"(Skill|Senses|Speed|Support Benefit|Advanced Maneuver)", r"</p><p><strong>\1</strong>", string)
    return string


def eidolon_format(string):
    string = sub(
        r"(Tradition|Traits|Alignment|Home Plane|Size|Suggested Attacks|Skills|Senses|Language|Speed|Eidolon Abilities)",
        r"</p><p><strong>\1</strong>", string)
    string = sub(
        r"(\w+) (\w+) Str (\d+), Dex (\d+), Con (\d+), Int (\d+), Wis (\d+), Cha (\d+); \+(\d+) AC \(\+(\d+) Dex cap\)",
        r"</p><p><strong>\1 \2</strong> Str \3, Dex \4, Con \5, Int \6, Wis \7, Cha \8; +\9 AC (+\10 Dex cap)", string)
    return string


def handle_inlines_checks(string):
    # Skills and saves
    string = sub(r"jet de (\w+) basique %s" % DC, r"@Check[type:\1|dc:\2|basic:true]", string)
    string = sub(r"%s %s" % (DC, SAVES), r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s %s" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"sauvegarde de %s \(%s\)" % (SAVES, DC), r"@Check[type:\1|dc:\2]", string)

    string = sub(r"%s %s" % (DC, SKILLS), r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s %s" % (SKILLS, DC), r"@Check[type:\1|dc:\2]", string)
    string = sub(r"%s \(%s\)" % (SKILLS, DC), r"@Check[type:\1|dc:\2", string)

    string = sub(r"(\w+) Lore %s" % DC, r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s (\w+) save" % DC, r"@Check[type:\2|dc:\1]", string)
    string = sub(r"%s flat check" % DC, r"@Check[type:flat|dc:\1]", string)

    # Catch capitalized saves
    string = sub(r"type:%s" % SAVES, convert_to_lower, string)
    string = sub(r"type:%s" % SKILLS, convert_to_lower, string)

    return LOCALIZE_PATTERN_SAVES_ROLLS.sub(lambda x: LOCALIZE_SAVES_ROLLS[x.group()], string)


def handle_counteract(string):
    string = sub(r"counteract modifier of \+(\d+)", r"counteract modifier of [[/r 1d20+\1 #Counteract]]{+\1}", string)
    string = sub(r"\+(\d+) counteract modifier", r"[[/r 1d20+\1 #Counteract]]{+\1} counteract modifier", string)
    return string


def ancestry_format(string):
    string = sub(r"(?i)Y\s*O\s*U M\s*I\s*G\s*H\s*T\s*...", r"</p><h2>You Might...</h2>", string)
    string = sub(r"O\s*T\s*H\s*E\s*R\s*S P\s*R\s*O\s*B\s*A\s*B\s*L\s*Y\s*...", r"</ul><h2>Others Probably...</h2><ul>",
                 string, flags=re.IGNORECASE)
    string = sub(r"(?i)P\s*H\s*Y\s*S\s*I\s*C\s*A\s*L D\s*E\s*S\s*C\s*R\s*I\s*P\s*T\s*I\s*O\s*N",
                 r"</ul><h2>Physical Description</h2><p>", string)
    string = sub(r"(?i)S\s*O\s*C\s*I\s*E\s*T\s*Y", r"</p><h2>Society</h2><p>", string)
    string = sub(r"(?i)A\s*L\s*I\s*G\s*N\s*M\s*E\s*N\s*T A\s*N\s*D R\s*E\s*L\s*I\s*G\s*I\s*O\s*N",
                 r"</p><h2>Alignment and religion</h2><p>", string)
    string = sub(r"NAMES", r"</p><h2>Names</h2><p>", string)
    string = sub(r"(?i)S\s*a\s*m\s*p\s*l\s*e N\s*a\s*m\s*e\s*S", r"</p><h3>Sample Names</h3><p>", string)
    return string


def handle_areas(string):
    string = sub(r" ([A-Z][0-9]{1,3})", r" <strong>\1</strong>", string)
    return string


def handle_innate_spell_links(string):
    string = sub(r"You can cast (\w+) (.*?) innate",
                 r"You can cast <em>@Compendium[pf2e.spells-srd.\1]{\1}</em> \2 innate", string)
    return string


def reformat(text, third_party=False, companion=False, eidolon=False, ancestry=False, use_clipboard=True,
             add_gm_text=True, inline_rolls=True, add_conditions=True, add_actions=True, add_inline_checks=True,
             add_inline_templates=True, remove_non_ASCII=True):
    # Initial handling not using regex.
    string = "<p>" + text.replace("Déclencheur", "<p><strong>Déclencheur</strong>") \
        .replace("\nSuccès critique", "</p><hr /><p><strong>Réussite critique</strong>") \
        .replace("\nSuccès", "</p><p><strong>Réussite</strong>") \
        .replace("\nÉchec critique", "</p><p><strong>Échec critique</strong>") \
        .replace("\nÉchec", "</p><p><strong>Échec</strong>") \
        .replace("\nSpécial", "</p><p><strong>Spécial</strong>") \
        .replace("\n", " ") \
        .replace("Fréquence", "<p><strong>Fréquence</strong>") \
        .replace("Effet", "</p><hr /><p><strong>Effet</strong>") \
        .replace("Coût", "<strong>Coût</strong>") + "</p>"
    string = string.replace("<p><p>", "<p>") \
        .replace(r"”", r'"') \
        .replace(r"“", r'"') \
        .replace("Durée maximale", "</p><p><strong>Durée maximale</strong>") \
        .replace("Délai", "</p><p><strong>Délai</strong>") \
        .replace("Jet de sauvegarde", "</p><p><strong>Jet de sauvegarde</strong>")

    if remove_non_ASCII:
        string = string.replace("’", "'")

    string = sub(r"(Condition|Conditions)", r"<p><strong>Conditions</strong>", string)

    string = sub(r"Stade (\d)", r"</p><p><strong>Stade \1</strong>", string)

    string = sub("Prérequis", "<p><strong>Prérequis</strong>", string, count=1)
    string = sub(r"Activation \?", r"</p><p><strong>Activation</strong> <span class='pf2-icon'>1</span>", string)

    if third_party:
        string = handle_third_party(string)

    if companion:
        string = companion_format(string)

    if eidolon:
        string = eidolon_format(string)

    if ancestry:
        string = ancestry_format(string)

    if add_inline_checks:
        string = handle_inlines_checks(string)

    if add_conditions:
        string = handle_conditions(string)

    if inline_rolls:
        string = handle_damage_rolls(string)

    if add_inline_templates:
        string = handle_templates(string)

    string = handle_spell_heightening(string)
    string = handle_bullet_lists(string)

    if add_actions:
        string = handle_actions(string)

    string = handle_equipment(string)
    string = handle_feats(string)
    string = handle_spells(string)
    # string = handle_innate_spell_links(string)
    string = handle_counteract(string)

    string = handle_activation_actions(string)
    string = handle_aura(string)

    string = handle_areas(string)

    if "Choose two ability boosts" in string:
        string = handle_background(string)

    string = string.replace("<p></p>", "").replace("<p><p>", "<p>")
    string = string.replace(" <p>", "</p><p>")
    string = string.replace(" </p>", "</p>")
    string = string.replace(";</p>", "</p>")
    string = string.replace("<p> ", "<p>")

    # Sneak attack features have different text requirements so we undo some of the changes made
    string = sub(
        r"deals an additional \[\[/r {(\d)d(\d)}\[precision\]\]\]{(\d)d(\d) precision damage} to @Compendium\[pf2e.conditionitems.Flat-Footed\]{Flat-Footed} creatures.",
        r"deals an additional \1d\2 precision damage to flat-footed creatures.", string)

    if add_gm_text:
        string = string.replace("<p><strong>Déclencheur</strong>",
                                "<p data-visibility='gm'><strong>Déclencheur</strong>")
        string = string.replace("<p><strong>Conditions</strong>", "<p data-visibility='gm'><strong>Conditions</strong>")
        string = string.replace("<p><strong>Fréquence</strong>", "<p data-visibility='gm'><strong>Fréquence</strong>")

    # print("\n")
    # print(string)

    if use_clipboard:
        copy(string)

    # return string
    outputText.delete("1.0", END)
    outputText.insert(END, string)


###############################################################################
# If you want to run the console version of this instead of the GUI comment out
# the outputText lines above and uncomment `return string`. Then comment out 
# everything below up to `def main()` then comment out `root.mainloop()` and 
# uncomment `reformat(...)`.
#
# Build with `pyinstaller --noconsole --icon="D20_icon.ico" --onefile dataEntry.py`
###############################################################################

def clearInput():
    inputText.delete("1.0", END)


Height = 700
Width = 800

root = Tk()

root.title("PF2e on Foundry VTT Data Entry v 2.5.2")

canvas = Canvas(root, height=Height, width=Width)
canvas.pack()

frame = Frame(root, bg='#80c0ff')
frame.place(relwidth=1, relheight=1)

inputText = Text(frame, bg='white')
inputText.place(rely=0.2, relwidth=0.49, relheight=0.8)

outputText = Text(frame, bg='white')
outputText.place(relx=0.51, rely=0.2, relwidth=0.49, relheight=0.8)

## Settings
###############################################################################
third_party = BooleanVar()
companion = BooleanVar()
eidolon = BooleanVar()
ancestry = BooleanVar()
use_clipboard = BooleanVar(value=True)
add_gm_text = BooleanVar(value=False)
inline_rolls = BooleanVar(value=True)
add_conditions = BooleanVar(value=True)
add_actions = BooleanVar(value=True)
add_inline_checks = BooleanVar(value=True)
add_inline_templates = BooleanVar(value=True)
remove_non_ASCII = BooleanVar(value=True)

# # handleThirdParty = Checkbutton(text = "Support Third Party", variable = third_party)
# # handleThirdParty.place(relx = 0.3, rely= 0)

# # handleCompanion = Checkbutton(text = "Animal Companion", variable = companion)
# # handleCompanion.place(relx = 0.3, rely= 0.05)

# # handleEidolon = Checkbutton(text = "Eidolon", variable = eidolon)
# # handleEidolon.place(relx = 0.3, rely= 0.1)

# # handleAncestry = Checkbutton(text = "Ancestry", variable = ancestry)
# # handleAncestry.place(relx = 0.5, rely= 0.0)

# # useClipboard = Checkbutton(text = "Copy Output to Clipboard", variable = use_clipboard)
# # useClipboard.place(relx = 0.5, rely= 0.05)
###############################################################################


# Build settings menu
##############################################################################

menu = Menu(root)

settings_menu = Menu(menu)
settings_menu.add_checkbutton(label="Copy Output to Clipboard", variable=use_clipboard)
settings_menu.add_checkbutton(label="Add GM Only Tags", variable=add_gm_text)
settings_menu.add_checkbutton(label="Handle Inline rolls", variable=inline_rolls)
settings_menu.add_checkbutton(label="Add Inline Templates", variable=add_inline_templates)
settings_menu.add_checkbutton(label="Add Inline Checks", variable=add_inline_checks)
settings_menu.add_checkbutton(label="Add Condition Links", variable=add_conditions)
settings_menu.add_checkbutton(label="Add Action Links", variable=add_actions)
settings_menu.add_checkbutton(label="Remove non-ASCII characters", variable=remove_non_ASCII)
settings_menu.add_checkbutton(label="Handle Animal Companion Blocks", variable=companion)
settings_menu.add_checkbutton(label="Handle Eidolon Blocks", variable=eidolon)
settings_menu.add_checkbutton(label="Handle Ancestry Description Text", variable=ancestry)
settings_menu.add_checkbutton(label="Handle Third Party Formatting", variable=third_party)

menu.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menu)

##############################################################################

reformatButton = Button(root, text="Reformat Text",
                        command=lambda: reformat(inputText.get("1.0", "end-1c"), third_party.get(), companion.get(),
                                                 eidolon.get(), ancestry.get(), use_clipboard.get(), add_gm_text.get(),
                                                 inline_rolls.get(), add_conditions.get(), add_actions.get(),
                                                 add_inline_checks.get(), add_inline_templates.get(),
                                                 remove_non_ASCII.get()))
reformatButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.2)

resetButton = Button(root, text="Clear Input", command=lambda: clearInput())
resetButton.place(relx=0, rely=0, relwidth=0.25, relheight=0.2)


def main():
    # reformat(input(), third_party = False, companion = False, eidolon = False, ancestry = False, use_clipboard=True, add_gm_text = False, inline_rolls = True, add_conditions = True, add_inline_checks = True, add_inline_templates = True, remove_non_ASCII = True)
    root.mainloop()


if __name__ == "__main__":
    main()
