# Consoletogui
This is  python code. It convert from console to gui
```markdown
# Console -> MyLibrary converter (Python 3.7+ compatible)

Bu konverter Python 3.7+ muhitida ham ishlaydi. Agar sizda Python 3.9 yoki undan yuqori bo'lsa, u ast.unparse dan foydalanadi. Aks holda astunparse yoki astor kerak bo'ladi.

O'rnatish:
- Python 3.7+ kerak.
- Agar Python < 3.9 bo'lsa, quyidagilardan birini o'rnating:
  pip install astunparse
  yoki
  pip install astor

Ishlatish:
  python converter.py input_script.py output_fg.py

Tavsiyalar:
- Agar kutubxonangizda inputs_number yoki MyLibrary API boshqacha bo'lsa, transformerda kerakli nomlarni o'zgartiraylik.
- Murakkab kodlar uchun (funktsiyalar ichidagi input, classlar, dynamic eval) qo'shimcha AST qoidalari qo'shish mumkin.
```
