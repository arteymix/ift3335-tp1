rapport.pdf: rapport.md
	pandoc $< -o $@
