clean:
	*.txt *.pyc

update:
	git --work-tree=NBA-Stats/ --git-dir=NBA-Stats/.git/ pull origin master

.PHONY: clean update
