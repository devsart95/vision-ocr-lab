"""Create blank, unscored forms for collecting consented real handwriting later."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def create(name: str, title: str, fields: list[str]) -> None:
    image = Image.new("RGB", (1400, 1800), "white")
    draw = ImageDraw.Draw(image)
    heading = ImageFont.load_default(size=42)
    body = ImageFont.load_default(size=28)
    draw.rectangle((35, 35, 1365, 1765), outline="#1a4962", width=4)
    draw.text((70, 70), title, font=heading, fill="#1a4962")
    draw.text((70, 145), "BLANK TEMPLATE - NOT SCORED IN THIS LAB", font=body, fill="black")
    for index, field in enumerate(fields):
        y = 240 + index * 125
        draw.text((70, y), field, font=body, fill="black")
        draw.line((70, y + 85, 1320, y + 85), fill="#7e9cac", width=2)
    draw.text(
        (70, 1650),
        "Use fictitious data or obtain consent. Website: justino.dev",
        font=body,
        fill="#1a4962",
    )
    image.save(ROOT / "templates" / (name + ".png"))


def main() -> None:
    create(
        "invoice-pyg",
        "Handwritten invoice collection - PYG",
        [
            "Supplier / recipient (fictitious)",
            "Invoice number / date",
            "Tax IDs (fictitious)",
            "Description / quantity / unit price",
            "Exempt / VAT 5% / VAT 10%",
            "Total / tax included",
            "Amount written in words",
            "Mark any unknown or occluded field",
        ],
    )
    create(
        "invoice-usd",
        "Handwritten invoice collection - USD",
        [
            "Supplier / recipient (fictitious)",
            "Invoice number / date",
            "Tax IDs (fictitious)",
            "Currency / decimal convention",
            "Description / quantity / unit price",
            "USD total / exchange rate / PYG equivalent",
            "Amount written in words",
            "Mark any unknown or occluded field",
        ],
    )
    create(
        "optical-reading",
        "Optical reading collection",
        [
            "Power in dBm (include sign)",
            "Wavelength in nm",
            "Displayed power in uW",
            "Latitude (include sign)",
            "Longitude (include sign)",
            "Timestamp / timezone",
            "Unknown or occluded readings",
            "Capture conditions / consent reference",
        ],
    )


if __name__ == "__main__":
    main()
