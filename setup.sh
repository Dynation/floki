#!/bin/bash

# Назва репозиторію
PROJECT_NAME="floki-lang"

# Створення кореневого каталогу
mkdir -p $PROJECT_NAME

# Структура репозиторію
mkdir -p $PROJECT_NAME/{docs,src,examples,tests,ai-analysis,community}

# Документація
touch $PROJECT_NAME/docs/{overview.md,syntax.md,bytecode.md,vm.md,compiler.md,ai-analysis.md}

# Вихідний код
mkdir -p $PROJECT_NAME/src/{compiler,vm}
touch $PROJECT_NAME/src/compiler/{lexer.ts,parser.ts,emitter.ts,runtime.ts}
touch $PROJECT_NAME/src/vm/{floki-vm.ts,memory.ts,sensors.ts,motors.ts}

# Приклади коду
touch $PROJECT_NAME/examples/{drone-control.floki,lawn-bot.floki,robotic-arm.floki}

# Тести
mkdir -p $PROJECT_NAME/tests/{unit,integration}
touch $PROJECT_NAME/tests/unit/{test-lexer.ts,test-parser.ts}
touch $PROJECT_NAME/tests/integration/{test-vm.ts,test-runtime.ts}

# Аналіз AI
touch $PROJECT_NAME/ai-analysis/{chatgpt.md,gemini.md,comparisons.md}

# Матеріали для спільноти
touch $PROJECT_NAME/community/{roadmap.md,contributing.md,faq.md}

# Основні файли
touch $PROJECT_NAME/{README.md,LICENSE,CONTRIBUTING.md}

# Запис README з описом проєкту
echo "# Floki: Мова для автономних систем" > $PROJECT_NAME/README.md
echo "Floki — це подієва мова програмування для робототехніки, створена для простого керування автономними пристроями." >> $PROJECT_NAME/README.md

# Виведення результату
echo "✅ Структура проєкту $PROJECT_NAME успішно створена!"
