ruff:
    uvx ruff check src --output-format=concise

ruff-fix:
    uvx ruff check src --fix --output-format=concise

format:
    uvx ruff format src --output-format=concise

build:
    rm -rf dist
    uv run pyinstaller \--onefile --windowed --icon resources/icons/msw_logo.ico --name MSW src/mysmartwallet/main.py
    mkdir dist/data/
    powershell Compress-Archive -Path dist\* -DestinationPath dist/MSW.zip
