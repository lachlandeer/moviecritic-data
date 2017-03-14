# Add paths for sub directories for source and output

init:
	$(shell mkdir -p src)
	$(shell mkdir -p out)

	# creating src subdirectories
	$(shell mkdir -p $(SRC)/lib)
	$(shell mkdir -p $(SRC)/main)

	# out sub-directories
	$(shell mkdir -p $(OUT)/links)
	$(shell mkdir -p $(OUT)/data)

# declare sub directores
SRC_LIB  = $(SRC)/lib
SRC_MAIN = $(SRC)/main

OUT_LINKS = $(OUT)/links
OUT_DATA  = $(OUT)/data
