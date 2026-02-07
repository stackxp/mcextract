## mcextract

A small tool for extracting minecraft assets

### Prerequisites

- Python 3
- Git (for downloading the repo)

### Usage

Extract files from multimc into a folder named `minecraft`:

```bash
python extract.py ~/.local/share/multimc/assets -o minecraft
```

You can also override the location of the object folder and index file like as follows: (Also, you can omit the output directory. This example will generate a folder named `output`)

```bash
python extract.py -i <path_to_index_file> -d <path_to_object_dir>
```
