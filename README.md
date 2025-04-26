# Captcha Solver

A local captcha solving solution that uses OCR (Optical Character Recognition) to process and solve captcha images without relying on external APIs.

## Features

- Local processing without external API dependencies
- Supports common captcha image formats
- Uses Tesseract OCR engine for text recognition
- Pre-processing filters to improve accuracy
- Easy to integrate with existing projects

## Requirements

- Python 3.7+
- Tesseract OCR
- OpenCV
- Pillow

## Installation

1. Clone the repository:
```bash
git clone https://github.com/begula-Inc/captcha-solver.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
- Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

## Usage

```python
from captcha_solver import solve_captcha

result = solve_captcha("path/to/captcha.png")
print(f"Solved captcha: {result}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.