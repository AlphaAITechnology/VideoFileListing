main: main.o 
	g++ @flags $^ -o $@

main.o: main.cpp
	g++ -c @flags $^




.PHONY: clean wipe format
clean:
	ls | grep -E ".*\.o$\" | xargs -I{} rm {}
wipe: clean
	rm main
format:
	clang-format -i main.cpp
	ls src/ | grep -E ".*\.((c|h)pp|h)$\" | xargs -I{} clang-format -i {}
	ls include/ | grep -E ".*\.((c|h)pp|h)$\" | xargs -I{} clang-format -i {}