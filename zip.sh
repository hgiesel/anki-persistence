declare DIR="$(cd "$(dirname "$0")" && pwd -P)"

mkdir -p "$DIR/build"
cp -f "$DIR/script.js" "$DIR/asset_manager/web"

if [[ "$1" =~ ^-?a$ ]]; then
  # for uploading to AnkiWeb
  declare addon_id=''
else
  # for installing myself
  declare addon_id='anki_persistence'
fi

cd "$DIR/asset_manager"
zip -r "$DIR/build/$addon_id.ankiaddon" \
  *".py" \
  "manifest.json" \
  "web/"*
