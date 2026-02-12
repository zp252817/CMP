#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "== CMP 知识地图启动器 =="
echo "工作目录: $ROOT_DIR"
echo

if [[ ! -x "./scripts/km" ]]; then
  echo "未找到可执行脚本: ./scripts/km"
  echo "请先检查项目目录是否完整。"
  echo
  read -r -p "按回车关闭..."
  exit 1
fi

echo "正在执行: 更新并打开知识地图..."
if ./scripts/km start; then
  echo
  echo "完成：知识地图已更新并尝试打开。"
else
  echo
  echo "执行失败，请查看上方日志。"
  read -r -p "按回车关闭..."
  exit 1
fi

echo
read -r -p "按回车关闭..."

