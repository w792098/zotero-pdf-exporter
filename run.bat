@echo off
chcp 65001 >nul
echo ======================================
echo   Zotero PDF 导出工具
echo ======================================
echo.
echo 请确保 Zotero 已经关闭！
echo.
python export_zotero_pdfs.py
echo.
pause