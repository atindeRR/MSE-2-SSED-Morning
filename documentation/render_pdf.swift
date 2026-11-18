import AppKit
import Foundation
import PDFKit

guard CommandLine.arguments.count == 3,
      let document = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1])) else {
    fatalError("usage: render_pdf <input.pdf> <output-directory>")
}

let output = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)

for index in 0..<document.pageCount {
    guard let page = document.page(at: index) else { continue }
    let bounds = page.bounds(for: .mediaBox)
    let scale: CGFloat = 2.0
    let image = NSImage(size: NSSize(width: bounds.width * scale, height: bounds.height * scale))
    image.lockFocus()
    NSColor.white.setFill()
    NSRect(origin: .zero, size: image.size).fill()
    guard let context = NSGraphicsContext.current?.cgContext else { fatalError("missing context") }
    context.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: context)
    image.unlockFocus()
    guard let data = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: data),
          let png = bitmap.representation(using: .png, properties: [:]) else { continue }
    let url = output.appendingPathComponent(String(format: "page-%02d.png", index + 1))
    try png.write(to: url)
}

print("rendered \(document.pageCount) pages")
