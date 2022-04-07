from draw.base import Position


class Text(Position):
    """
    simple text
    """
    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        #text_style: TextStyle = DEFAULT_TEXT_STYLE,
        text_anchor: str = "middle",
        text_dominant_baseline: str = "middle",
        class_: str = "default_text"
    ):
        Position.__init__(self, x, y)

        self.text = text
        self.text_anchor = text_anchor
        self.text_dominant_baseline = text_dominant_baseline
        #self.text_style = text_style
        self.class_ = class_

    def draw(self, dwg, grp=None):
        grp = grp or dwg

        grp.add(
            dwg.text(
                text=self.text,
                insert=(self.x, self.y),
                # fill=self.text_style.fill,
                # font_size=self.text_style.font_size,
                # font_family=self.text_style.font_family,
                # font_weight=self.text_style.font_weight,
                text_anchor=self.text_anchor,
                dominant_baseline=self.text_dominant_baseline,
                class_=self.class_
            )
        )

        return grp
