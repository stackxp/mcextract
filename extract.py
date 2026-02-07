import os, shutil, argparse, json, time

class AssetExtractor:
	def __init__(self, index_path: str, object_path : str) -> None:
		self.index_path: str = index_path
		self.object_path: str = object_path
		if not os.path.isdir(object_path):
			raise NotADirectoryError(f"{object_path} either doesn't exist or it is a file")
		try:
			with open(self.index_path) as file:
				files = json.load(file)["objects"]
			assert isinstance(files, dict)
			
			self.files: dict[str, str] = {k: v["hash"] for k, v in files.items()}
		except Exception as e:
			raise ValueError(f"The index file couldn't be read ({e})")

	def extract_asset(self, name: str, output_path: str):
		hash = self.files.get(name)
		if not hash:
			raise FileNotFoundError(f"The asset \"{name}\" couldn't be found")
		actual_path = os.path.join(self.object_path, hash[:2], hash)
		shutil.copy2(actual_path, output_path)

	def extract_all(self, output_dir: str):
		if not os.path.exists(output_dir):
			os.mkdir(output_dir)
		for name in self.files:
			outpath = os.path.join(output_dir, name.lstrip("/"))
			os.makedirs(os.path.dirname(outpath), exist_ok=True)
			self.extract_asset(name, outpath)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("asset_dir", nargs="?", help="The \"asset\" folder in the \".minecraft\" directory")
	parser.add_argument("-o", '--output', default="output", help="The directory to put the extracted files in")
	parser.add_argument("-i", "--index-file", type=str, default="", help="Override the path to the object index file")
	parser.add_argument("-d", "--object-dir", type=str, default="", help="Override the path to the \"objects\" directory")
	args = parser.parse_args()

	object_dir = str(args.object_dir)
	index_file = str(args.index_file)
	asset_dir = str(args.asset_dir)
	output_dir = str(args.output)

	if (not index_file or not object_dir) and not os.path.exists(asset_dir):
		print("Error: Please supply either ASSET_DIR or --index-file and --object-dir")
		parser.print_help()
		exit(1)

	if not index_file:
		index_dir = os.path.join(asset_dir, "indexes")
		if not os.path.isdir(index_dir):
			print(f'Error: "{index_dir}" is not a directory')
			exit(1)
		files = list(filter(lambda f: f.endswith(".json"), os.listdir(index_dir)))
		if len(files) == 0:
			print(f'Error: No index files found in "{index_dir}"')
			exit(1)
		index_file = os.path.join(index_dir, files[0])
		print(f'Using "{index_file}" as the index file')

	if not object_dir:
		object_dir = os.path.join(asset_dir, "objects")
		if not os.path.isdir(object_dir):
			print(f'"Error: "{object_dir}" is not a directory')
			exit(1)
		print(f'Using "{object_dir}" as the object directory')

	start = time.time()
	ex = AssetExtractor(index_file, object_dir)
	ex.extract_all(output_dir)
	print(f"Extracted {len(ex.files)} files in {round(time.time() - start, 2)} seconds")

if __name__ == "__main__":
	main()
