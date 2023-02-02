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

ACTIONS = ["(Être|Est) furtif", "Garder? l’équilibre", "Contrain(dre|t)", "Ramper?", "Fai(re|t) diversion",
           "Démoraliser?", "Désamorcer? un dispositif", "Désarmer?", "Gagner? de l’argent", "S'échapper?", "Feinter?",
           "Forcer? l'ouverture", "Se raccrocher? in extremis", "Saisi(r|t)", "Sauter? en hauteur",
           "Sauter? en longueur", "Bondi(r|t)", "Pas libérateur", "Fai(re|t) bonne impression", "Se met(tre)? en selle",
           "Se produi(re|t)", "Chercher?", "Fouiller?", "Deviner? les intentions", "Pousser?", "Se cacher?", "Voler?",
           "Vol", "Mise à l'abri", "Pister?", "Soigner? les maladies", "Soigner? un empoisonnement",
           "Soigner? les blessures", "Croc-en-jambe", "Déplacement acrobatique"]

CONDITIONS = ["Aveuglée?s?", "Fatiguée?s?", "Confuse?s?", "Masquée?s?", "Éblouie?s?", "Sourde?s?", "Invisibles?",
              "Prise?s? au dépourvu", "Immobilisée?s?", "Á terre", "Inconsciente?s?", "Fascinée?s?", "Paralysée?s?",
              "Cachée?s?", "Accélérée?s?", "En fuite", "Empoignée?s?", "Entravée?s?"]

NUMBERED_CONDITIONS = ["Maladroite?s?", "Condamnée?s?", "Drainée?s?", "Affaiblie?s?", "Ralentie?s?", "Effrayée?s?",
                       "Malades?", "Étourdie?s?", "Stupéfiée?s?", "Accélérée?s?"]

LOCALIZE_ACTIONS = {
    "(Être|Est) furtif": "Compendium.pf2e.actionspf2e.VMozDqMMuK5kpoX4",
    "Garder? l’équilibre": "Compendium.pf2e.actionspf2e.M76ycLAqHoAgbcej",
    "Contrain(dre|t)": "Compendium.pf2e.actionspf2e.tHCqgwjtQtzNqVvd",
    "Ramper?": "Compendium.pf2e.actionspf2e.Tj055UcNm6UEgtCg",
    "Fai(re|t) diversion": "Compendium.pf2e.actionspf2e.GkmbTGfg8KcgynOA",
    "Démoraliser?": "Compendium.pf2e.actionspf2e.2u915NdUyQan6uKF",
    "Désamorcer? un dispositif": "Compendium.pf2e.actionspf2e.cYdz2grcOcRt4jk6",
    "Désarmer?": "Compendium.pf2e.actionspf2e.Dt6B1slsBy8ipJu9",
    "Gagner? de l’argent": "Compendium.pf2e.actionspf2e.QyzlsLrqM0EEwd7j",
    "S'échapper?": "Compendium.pf2e.actionspf2e.SkZAQRkLLkmBQNB9",
    "Feinter?": "Compendium.pf2e.actionspf2e.QNAVeNKtHA0EUw4X",
    "Forcer? l'ouverture": "Compendium.pf2e.actionspf2e.SjmKHgI7a5Z9JzBx",
    "Se raccrocher? in extremis": "Compendium.pf2e.actionspf2e.3yoajuKjwHZ9ApUY",
    "Saisi(r|t)": "Compendium.pf2e.actionspf2e.PMbdMWc2QroouFGD",
    "Sauter? en hauteur": "Compendium.pf2e.actionspf2e.2HJ4yuEFY1Cast4h",
    "Sauter? en longueur": "Compendium.pf2e.actionspf2e.JUvAvruz7yRQXfz2",
    "Bondi(r|t)": "Compendium.pf2e.actionspf2e.d5I6018Mci2SWokk",
    "Pas libérateur": "Compendium.pf2e.actionspf2e.IX1VlVCL5sFTptEE",
    "Fai(re|t) bonne impression": "Compendium.pf2e.actionspf2e.OX4fy22hQgUHDr0q",
    "Se met(tre)? en selle": "Compendium.pf2e.actionspf2e.PM5jvValFkbFH3TV",
    "Se produi(re|t)": "Compendium.pf2e.actionspf2e.EEDElIyin4z60PXx",
    "Chercher?": "Compendium.pf2e.actionspf2e.BlAOM2X92SI6HMtJ",
    "Fouiller?": "Compendium.pf2e.actionspf2e.TiNDYUGlMmxzxBYU",
    "Deviner? les intentions": "Compendium.pf2e.actionspf2e.1xRFPTFtWtGJ9ELw",
    "Pousser?": "Compendium.pf2e.actionspf2e.7blmbDrQFNfdT731",
    "Se cacher?": "Compendium.pf2e.actionspf2e.XMcnh4cSI32tljXa",
    "Voler?": "Compendium.pf2e.actionspf2e.RDXXE7wMrSPCLv5k",
    "Vol": "Compendium.pf2e.actionspf2e.cS9nfDRGD83bNU1p",
    "Mise à l'abri": "Compendium.pf2e.actionspf2e.ust1jJSCZQUhBZIz",
    "Pister?": "Compendium.pf2e.actionspf2e.EA5vuSgJfiHH7plD",
    "Soigner? les maladies": "Compendium.pf2e.actionspf2e.TC7OcDa7JlWbqMaN",
    "Soigner? un empoisonnement": "Compendium.pf2e.actionspf2e.KjoCEEmPGTeFE4hh",
    "Soigner? les blessures": "Compendium.pf2e.actionspf2e.1kGNdIIhuglAjIp9",
    "Croc-en-jambe": "Compendium.pf2e.actionspf2e.ge56Lu1xXVFYUnLP",
    "Déplacement acrobatique": "Compendium.pf2e.actionspf2e.21WIfSu7Xd7uKqV8"
}

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

LOCALIZE_TEMPLATES = {
    "type:émanation": "type:emanation",
    "type:explosion": "type:burst",
    "type:cône": "type:cone",
    "type:ligne": "type:line"
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
    return sub(r"\b(" + action + r")\b",
               r"@UUID[%s]{\g<0>}" % LOCALIZE_ACTIONS[action],
               string, count=1)


def condition_sub(string, condition):
    return sub(condition.lower(),
               r"%s%s]{\g<0>}" % (CONDITION_COMPENDIUM, LOCALIZE_CONDITIONS[condition]),
               string, count=1)


def condition_sub_with_stage(string, condition, stage):
    return sub(r"%s %s" % (condition.lower(), stage),
               r"%s%s]{\g<0>}" % (CONDITION_COMPENDIUM, LOCALIZE_CONDITIONS[condition]),
               string, count=1)


def handle_actions(string):
    for action in ACTIONS:
        string = action_sub(string, action)
    return string


def handle_conditions(string):
    for condition in CONDITIONS:
        string = condition_sub(string, condition)

    # Handle this one manually due to the lack of hyphen.
    string = sub(r"pris au dépourvu", r"%sAJh5ex99aV6VTggg]{Pris au dépourvu}" % CONDITION_COMPENDIUM, string, count=1)

    for condition in NUMBERED_CONDITIONS:
        for i in range(1, 6):
            string = condition_sub_with_stage(string, condition, i)
    return string


def handle_damage_rolls(string):
    string = sub(r" (\d)d(\d) (rounds|minutes|heures|jours)", r" [[/r \1d\2 #\3]]{\1d\2 \3}", string)
    string = sub(r"(\d+)(d\d+)?(\+\d+)? dégât(s)?( d\'éclaboussures?)?(\sde\s|\sd\'|\s)(\w*)( persistants?)?",
                 lambda x: f"[[/r "
                           f"{'(' if x.group(3) is not None else ''}"
                           f"{x.group(1)}{x.group(2) or ''}{x.group(3) or ''}"
                           f"{')' if x.group(3) is not None else ''}"
                           f"[{'persistent,' if x.group(8) is not None else ''}"
                           f"{'splash,' if x.group(5) is not None else ''}"
                           f"{LOCALIZE_DAMAGE[x.group(7)] if x.group(7) in LOCALIZE_DAMAGE else ''}]]]"
                           f"{{{x.group(1)}{x.group(2) or ''}{x.group(3) or ''} dégât"
                           f"{x.group(4) if x.group(4) is not None else ''}"
                           f"{x.group(5) if x.group(5) is not None else ''}"
                           f"{x.group(6) + x.group(7) if x.group(7) in LOCALIZE_DAMAGE else ''}"
                           f"{x.group(8) or ''}}}{x.group(6) + x.group(7) if x.group(7) not in LOCALIZE_DAMAGE else ''}"
                 , string)
    string = sub(r"(\d+)(d\d+)?(\+\d+)? point(s)? de vie",
                 lambda x: f"[[/r "
                           f"{'(' if x.group(3) is not None else ''}"
                           f"{x.group(1)}{x.group(2) or ''}{x.group(3) or ''}"
                           f"{')' if x.group(3) is not None else ''}"
                           f"[healing]]]"
                           f"{{{x.group(1)}{x.group(2) or ''}{x.group(3) or ''} point"
                           f"{x.group(4) if x.group(4) is not None else ''}"
                           f" de vie}}"
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
    string = sub(r"•", "<ul>\n<li>", string, count=1)
    string = sub(r"•", "</li>\n<li>", string)
    return string


def handle_templates(string):
    # Add template buttons
    string = sub(r"(émanation|explosion|cône|ligne|Émanation|Explosion|Cône|Ligne) de (\d+\,?\d?) (mètres|m)",
                 r"@Template[type:\1|distance:\2]", string)
    string = sub(r"type:%s" % r"(Émanation|Explosion|Cône|Ligne)", convert_to_lower, string)
    string = sub(r"distance:(\d+\,?\d?)(]|\|)",
                 lambda x: "distance:" + str(int(float(x.group(1).replace(",", ".")) * 10 / 3)) + x.group(2), string)

    return LOCALIZE_PATTERN_TEMPLATES.sub(lambda x: LOCALIZE_TEMPLATES[x.group()], string)


def handle_aura(string):
    string = sub(r"<p>(\d+) m.",
                 lambda x: "<p>@UUID[Compendium.pf2e.bestiary-ability-glossary-srd.v61oEQaDdcRpaZ9X]{Aura} " +
                           "@Template[type:emanation|distance:" +
                           str(int(float(x.group(1).replace(",", ".")) * 10 / 3)) + "]{" + x.group(1) +
                           " m}</p>\n<hr />\n<p>",
                 string)
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

def handle_areas(string):
    string = sub(r" ([A-Z][0-9]{1,3})", r" <strong>\1</strong>", string)
    return string

def reformat(text, third_party=False, companion=False, eidolon=False, ancestry=False, use_clipboard=True,
             add_gm_text=True, inline_rolls=True, add_conditions=True, add_actions=True, add_inline_checks=True,
             add_inline_templates=True, remove_non_ASCII=True):
    # Initial handling not using regex.
    string = "<p>" + text.replace("Déclencheur.", "<p><strong>Déclencheur</strong>") \
        .replace("\n", " ") \
        .replace("Succès critique.", "</p>\n<hr />\n<p><strong>Succès critique</strong>") \
        .replace("Succès.", "</p>\n<p><strong>Succès</strong>") \
        .replace("Échec critique.", "</p>\n<p><strong>Échec critique</strong>") \
        .replace("Échec.", "</p>\n<p><strong>Échec</strong>") \
        .replace("Spécial.", "</p>\n<p><strong>Spécial</strong>") \
        .replace("Fréquence", "<p><strong>Fréquence</strong>") \
        .replace("Effet.", "</p>\n<hr /><p><strong>Effet</strong>") \
        .replace("Coût", "<strong>Coût</strong>") + "</p>"
    string = string.replace("<p><p>", "<p>") \
        .replace(r"”", r'"') \
        .replace(r"“", r'"') \
        .replace("Durée maximale", "</p>\n<p><strong>Durée maximale</strong>") \
        .replace("Délai", "</p>\n<p><strong>Délai</strong>") \
        .replace("Jet de sauvegarde", "</p>\n<hr />\n<p><strong>Jet de sauvegarde</strong>")

    if remove_non_ASCII:
        string = string.replace("’", "'")

    string = sub(r"(Condition(s)?)", r"<p><strong>Conditions</strong>", string)

    string = sub(r"Stade (\d)", r"</p><p><strong>Stade \1</strong>", string)

    string = sub("Prérequis", "<p><strong>Prérequis</strong>", string, count=1)
    string = sub(r"Activation \?", r"</p><p><strong>Activation</strong> <span class='pf2-icon'>1</span>", string)

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

    string = handle_aura(string)
    string = handle_areas(string)

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
                                "<p><strong>Déclencheur</strong>")
        string = string.replace("<p><strong>Conditions</strong>", "<p><strong>Conditions</strong>")
        string = string.replace("<p><strong>Fréquence</strong>", "<p><strong>Fréquence</strong>")

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

root.title("Foundry VTT Data Entry French v 1.1.0")

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
use_clipboard = BooleanVar(value=True)
add_gm_text = BooleanVar(value=False)
inline_rolls = BooleanVar(value=True)
add_conditions = BooleanVar(value=True)
add_actions = BooleanVar(value=True)
add_inline_checks = BooleanVar(value=True)
add_inline_templates = BooleanVar(value=True)
remove_non_ASCII = BooleanVar(value=True)

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

menu.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menu)

##############################################################################

reformatButton = Button(root, text="Reformat Text",
                        command=lambda: reformat(inputText.get("1.0", "end-1c"), use_clipboard.get(), add_gm_text.get(),
                                                 inline_rolls.get(), add_conditions.get(), add_actions.get(),
                                                 add_inline_checks.get(), add_inline_templates.get(),
                                                 remove_non_ASCII.get()))
reformatButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.2)

resetButton = Button(root, text="Clear Input", command=lambda: clearInput())
resetButton.place(relx=0, rely=0, relwidth=0.25, relheight=0.2)


def main():
    root.mainloop()


if __name__ == "__main__":
    main()
