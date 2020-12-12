all: main.cpp
	emcc main.cpp -std=c++11 -s WASM=1 -s USE_SDL=2 -O3 -o index.js --embed-file cube.vs cube.fs

clean:
	rm index.wasm index.js