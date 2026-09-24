
from pathlib import Path
from PIL import Image

# ============================================================
# SETTINGS
# ============================================================

ASSETS_DIR = Path(__file__).parent / "assets"

# 95 = extremely high quality
# 90 = excellent quality + good compression
# 85 = smaller files + still very good quality
WEBP_QUALITY = 90


# ============================================================
# IMAGE SETTINGS
# ============================================================

SUPPORTED = {
    ".jpg",
    ".jpeg",
    ".png",
}

SKIP = {
    ".webp",
    ".svg",
    ".avif",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".ico",
}


# ============================================================
# FORMAT SIZE
# ============================================================

def size_mb(size):
    return size / (1024 * 1024)


# ============================================================
# CONVERT IMAGE
# ============================================================

def convert_image(source: Path):

    destination = source.with_suffix(".webp")

    print(f"\n🖼️  {source.name}")

    try:

        # ----------------------------------------------------
        # Open original
        # ----------------------------------------------------

        with Image.open(source) as image:

            original_width, original_height = image.size

            print(
                f"   Resolution: "
                f"{original_width} × {original_height}"
            )

            # ------------------------------------------------
            # IMPORTANT:
            # NO resize happens anywhere in this script.
            # ------------------------------------------------

            # Preserve transparency
            if image.mode in ("RGBA", "LA"):

                converted = image

            elif image.mode == "P":

                if "transparency" in image.info:
                    converted = image.convert("RGBA")
                else:
                    converted = image.convert("RGB")

            else:

                converted = image.convert("RGB")

            # ------------------------------------------------
            # Save WebP
            # ------------------------------------------------

            converted.save(
                destination,
                "WEBP",
                quality=WEBP_QUALITY,
                method=6,
                optimize=True,
            )

        # ----------------------------------------------------
        # Verify WebP
        # ----------------------------------------------------

        with Image.open(destination) as webp:

            new_width, new_height = webp.size

        # Make absolutely sure resolution didn't change
        if (
            original_width != new_width
            or original_height != new_height
        ):

            print("   ❌ Resolution mismatch!")
            destination.unlink()

            return False

        # ----------------------------------------------------
        # File sizes
        # ----------------------------------------------------

        original_size = source.stat().st_size
        new_size = destination.stat().st_size

        saved = (
            (original_size - new_size)
            / original_size
        ) * 100

        print(
            f"   Original: "
            f"{size_mb(original_size):.2f} MB"
        )

        print(
            f"   WebP:     "
            f"{size_mb(new_size):.2f} MB"
        )

        print(
            f"   Saved:    "
            f"{saved:.1f}%"
        )

        # ----------------------------------------------------
        # DELETE ORIGINAL
        # ----------------------------------------------------

        source.unlink()

        print("   🗑️  Original deleted")
        print("   ✅ WebP created")

        return True

    except Exception as e:

        print(f"   ❌ ERROR: {e}")

        # Delete incomplete WebP if one was created
        if destination.exists():

            try:
                destination.unlink()
            except:
                pass

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("        🚀 WEBSITE WEBP IMAGE OPTIMIZER")
    print("=" * 60)

    print(f"\n📁 Assets folder:")
    print(f"   {ASSETS_DIR}")

    # --------------------------------------------------------
    # Check assets folder
    # --------------------------------------------------------

    if not ASSETS_DIR.exists():

        print("\n❌ Assets folder doesn't exist!")

        print(
            "\nCreate this structure:\n"
            "YourProject/\n"
            "├── app.py\n"
            "└── assets/\n"
        )

        return

    # --------------------------------------------------------
    # Find files
    # --------------------------------------------------------

    files = list(ASSETS_DIR.rglob("*"))

    converted = 0
    skipped = 0
    errors = 0

    # --------------------------------------------------------
    # Process
    # --------------------------------------------------------

    for file in files:

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        # ----------------------------------------------------
        # Existing WebP
        # ----------------------------------------------------

        if extension == ".webp":

            print(
                f"⏭️  Skipping WebP: "
                f"{file.relative_to(ASSETS_DIR)}"
            )

            skipped += 1
            continue

        # ----------------------------------------------------
        # SVG
        # ----------------------------------------------------

        if extension == ".svg":

            print(
                f"⏭️  Skipping SVG: "
                f"{file.relative_to(ASSETS_DIR)}"
            )

            skipped += 1
            continue

        # ----------------------------------------------------
        # Other unsupported files
        # ----------------------------------------------------

        if extension not in SUPPORTED:

            continue

        # ----------------------------------------------------
        # Convert
        # ----------------------------------------------------

        if convert_image(file):

            converted += 1

        else:

            errors += 1

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print("                    COMPLETE")
    print("=" * 60)

    print(f"✅ Converted : {converted}")
    print(f"⏭️  Skipped   : {skipped}")
    print(f"❌ Errors    : {errors}")

    print()
    print("📁 All WebP files are inside:")
    print(f"   {ASSETS_DIR}")

    print()
    print("🎉 Done!")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
