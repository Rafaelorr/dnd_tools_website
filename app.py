from flask import Flask, render_template, request, redirect, url_for, session
from helper_functies import get_max_spell_slots, roll_dice

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY"

def save_spell_slots_to_session(spell_slots):
    """Save spell slots to the Flask session."""

    session["spell_slots"] = {
        f"level_{i}": spell_slots.get(f"level_{i}", 0)
        for i in range(1, 10)
    }


@app.route("/")
def home():
    return redirect(url_for("spell_slot_tracker"))


@app.route("/spell_slot_tracker", methods=["GET", "POST"])
def spell_slot_tracker():
    if request.method == "POST":
        character_class = request.form.get("class")
        character_level = int(request.form.get("level"))

        # Save character information
        session["class"] = character_class
        session["character_level"] = character_level

        # Calculate maximum spell slots
        max_spell_slots = get_max_spell_slots(character_class,character_level)

        # Save maximum spell slots
        session["max_spell_slots"] = {
            f"level_{i}": max_spell_slots.get(f"level_{i}", 0)
            for i in range(1, 10)
        }

        # A new class/level means a fresh set of spell slots
        save_spell_slots_to_session(max_spell_slots)

        return redirect(url_for("spell_slot_tracker"))


    # ---------------------------------------------------------
    # LOAD DATA FROM SESSION
    # ---------------------------------------------------------

    character_class = session.get("class")
    character_level = session.get("character_level")

    max_spell_slots = session.get(
        "max_spell_slots",
        {}
    )

    spell_slots = session.get(
        "spell_slots",
        {}
    )


    # Determine whether the selected class is a caster
    track_spell_slots = bool(max_spell_slots)


    return render_template(
        "spell_slot_tracker.html",

        character_class=character_class,
        character_level=character_level,

        max_spell_slots=max_spell_slots,
        spell_slots=spell_slots,

        track_spell_slots=track_spell_slots
    )


@app.route("/spell_slot_tracker_save_slots", methods=["POST"])
def spell_slot_tracker_save_slots():

    # ---------------------------------------------------------
    # SAVE CURRENT SPELL SLOTS
    # ---------------------------------------------------------

    current_spell_slots = {}

    for i in range(1, 10):

        current_spell_slots[f"level_{i}"] = int(
            request.form.get(f"level_{i}", 0)
        )

    save_spell_slots_to_session(current_spell_slots)

    return redirect(url_for("spell_slot_tracker"))


@app.route("/spell_slot_tracker_long_rest", methods=["POST"])
def spell_slot_tracker_long_rest():

    # ---------------------------------------------------------
    # LONG REST: RESET CURRENT SLOTS TO MAXIMUM
    # ---------------------------------------------------------

    max_spell_slots = session.get(
        "max_spell_slots",
        {}
    )

    save_spell_slots_to_session(max_spell_slots)

    return redirect(url_for("spell_slot_tracker"))

@app.route("/dice_roller", methods=["GET", "POST"])
def dice_roller():
    if request.method == "POST":
        try:
            dice :int = int(request.form.get("dice"))
            amount :int = int(request.form.get("aantal"))
            mode :str = request.form.get("extra")
            modifier :int = int(request.form.get("modifier"))

            total :int = sum(roll_dice(dice, mode) for _ in range(amount)) + modifier

            result_text :str = f"{amount}d{dice} met {mode} = {total}"

            return render_template("dice_roller.html", resultaat=result_text)

        except Exception as ex:
            resultaat = f"Er is een fout gebeurd. Error: {ex}"

            return render_template("dice_roller.html", resultaat=resultaat)

    return render_template("dice_roller.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)