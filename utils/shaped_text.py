"""HarfBuzz-shaped Tibetan labels for Matplotlib's path-based renderer."""
from functools import lru_cache
from pathlib import Path
import numpy as np

@lru_cache(maxsize=256)
def glyph_path(text, font_file):
    import uharfbuzz as hb
    from fontTools.ttLib import TTFont
    from fontTools.pens.basePen import BasePen
    from matplotlib.path import Path as MplPath
    font = TTFont(font_file)
    glyphs = font.getGlyphSet()
    vertices, codes = [], []
    class Pen(BasePen):
        def _moveTo(self, p): vertices.append(p); codes.append(MplPath.MOVETO)
        def _lineTo(self, p): vertices.append(p); codes.append(MplPath.LINETO)
        def _curveToOne(self, p1,p2,p3): vertices.extend([p1,p2,p3]); codes.extend([MplPath.CURVE4]*3)
        def _qCurveToOne(self,p1,p2): vertices.extend([p1,p2]); codes.extend([MplPath.CURVE3]*2)
        def _closePath(self): vertices.append((0,0)); codes.append(MplPath.CLOSEPOLY)
    face = hb.Face(Path(font_file).read_bytes()); shaped = hb.Font(face)
    buffer = hb.Buffer(); buffer.add_str(text); buffer.guess_segment_properties()
    hb.shape(shaped, buffer)
    x,y = 0,0
    from fontTools.pens.transformPen import TransformPen
    pen=Pen(glyphs)
    for info,pos in zip(buffer.glyph_infos,buffer.glyph_positions):
        glyphs[font.getGlyphName(info.codepoint)].draw(TransformPen(pen,(1,0,0,1,x+pos.x_offset,y+pos.y_offset)))
        x += pos.x_advance; y += pos.y_advance
    font.close()
    return MplPath(np.array(vertices), codes), x, face.upem

def shape_artist(artist, font_file):
    """Retain Matplotlib layout/rotation while drawing correctly shaped glyphs."""
    from matplotlib.text import Text
    from matplotlib.transforms import Affine2D
    from matplotlib import colors
    class ShapedText(type(artist)):
        def draw(self, renderer):
            if not self.get_visible() or not self.get_text(): return
            if hasattr(self, 'update_positions'):
                self._renderer = renderer
                if not self._check_xy(renderer):
                    return
                self.update_positions(renderer)
            path, advance, units = glyph_path(self.get_text().replace('\n',' '), str(font_file))
            scale = renderer.points_to_pixels(self.get_fontsize())/units
            width = advance*scale
            bbox=path.get_extents(); height=bbox.height*scale
            x,y=self.get_transform().transform(self.get_position())
            dx={'left':0,'center':-width/2,'right':-width}.get(self.get_ha(),0)
            dy={'baseline':0,'bottom':-bbox.ymin*scale,'top':-bbox.ymax*scale,'center':-(bbox.ymin+bbox.ymax)*scale/2,'center_baseline':-height/2}.get(self.get_va(),0)
            transform=Affine2D().scale(scale).translate(dx,dy).rotate_deg(self.get_rotation()).translate(x,y)
            gc=renderer.new_gc();gc.set_linewidth(0);gc.set_foreground(colors.to_rgba(self.get_color(),self.get_alpha()))
            renderer.draw_path(gc,path,transform,rgbFace=colors.to_rgba(self.get_color(),self.get_alpha()))
            gc.restore()
    artist.__class__ = ShapedText
