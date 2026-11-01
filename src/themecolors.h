// Theme-aware colour mapping shared by diagrams and rich text.
//
// Light theme: colours are used exactly as in the original course.
// Dark theme: the HSL lightness of every colour is inverted onto the
// [background, foreground] range, so black ink becomes light text, white
// paper becomes the dark background and saturated colours keep their hue
// while staying readable.
#pragma once

#include <QColor>
#include <QString>

namespace ThemeColors {

// Background ("paper") colour of each theme.
QColor paper(bool dark);
// Default ink colour of each theme.
QColor ink(bool dark);

// Map a colour authored for a white page onto the requested theme.
QColor map(const QColor &c, bool dark);

// Map every #rrggbb colour found in an HTML fragment.
QString mapHtml(const QString &html, bool dark);

} // namespace ThemeColors
