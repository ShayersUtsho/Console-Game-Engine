// 3dcligametest.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <Windows.h>
#include <fstream>
#include<cstdlib>
#include<conio.h>
#include<cstring>
#include<ios>

#define L 31
#define B 31
#define EW 30
#define EH 16
#define TL 4
#define TB 4
#define FOV 1.7951958020513104219

using namespace std;

float pi = 3.14159265f;

POINT p;

//Display
int nDisplayWidth = 1920;
int nDisplayHeight = 1080;

//Render Options
bool wallCreases = true;
bool showMap = true;

//Map
int nMapHeight = 31;
int nMapWidth = 31;

//Map Design Presets
bool boundary = true;
int boundaryClearance = 0;
bool pillars = true;
int pillarInterval = 2;
int pInterval = pillarInterval + 1;

//Player
//float fPlayerX = (float)nMapWidth / 2.0;
//float fPlayerY = (float)nMapHeight / 2.0;
float fPlayerX = 1.0;
float fPlayerY = 1.0;
float fPlayerA = 0.0f;
float zAngle = 0.0f;

//Controls
float fHorizontalRotation = 2.0f;   //reduce when vertical movement is greater
float fVerticalRotation = 180.0f;   //reduce when horizontal movement is greater

//Camera
float fFOV = FOV;
float fFOVmin = pi / 6;
float fFOVmax = pi * 2;
float vFOV = 3;
float fDepth = (((float)nMapHeight) + ((float)nMapWidth)) / 2.0;

const char* mapname = "..\\Resources\\level-17.txt";
const char* texturename = "..\\Resources\\texture-5.txt";
int numberofMaps = 0;

void renamemap(char(&name)[24], int level) {
    for (int i = 0; i < strlen(mapname); i++) {
        name[i] = mapname[i];
    }
    name[19] = char(48 + level / 10);
    name[20] = char(48 + level % 10);
}

void renametexture(char(&name)[24], int level) {
    for (int i = 0; i < strlen(texturename); i++) {
        name[i] = texturename[i];
    }
    name[19] = char(48 + level / 10);
    name[20] = char(48 + level % 10);
}

void maximize() {
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    COORD NewSBSize = GetLargestConsoleWindowSize(hOut);
    SMALL_RECT DisplayArea = {0, 0, 0, 0};
    SetConsoleScreenBufferSize(hOut, NewSBSize);
    DisplayArea.Right = NewSBSize.X - 1;
    DisplayArea.Bottom = NewSBSize.Y - 1;
    SetConsoleWindowInfo(hOut, TRUE, &DisplayArea);
}

void preset(char map[L][B]) {
    for (int x = 0; x < L; x++) {
        for (int y = 0; y < B; y++) {
            if (x == 0 + boundaryClearance || y == 0 + boundaryClearance || x == L - 1 - boundaryClearance || y == B - 1 - boundaryClearance)
                map[x][y] = '#';
            else if (x % pInterval == boundaryClearance && y % pInterval == boundaryClearance)
                map[x][y] = '#';
            else
                map[x][y] = '.';
        }
    }
}

void texturepreset(char map[TL][TB]) {
    for (int x = 0; x < TL; x++) {
        for (int y = 0; y < TB; y++) {
            map[x][y] = ' ';
        }
    }
}

void display(char map[L][B]) {
    system("cls");
    for (int x = 0; x < L; x++) {
        for (int y = 0; y < B; y++) {
            cout << map[x][y];
        }
        cout << endl;
    }
}

void displayTexture(char map[TL][TB], char type) {
    system("cls");
    cout << "Texture for ";
    switch (type) {
    case '*':
        cout << "Player";
        break;
    case 'e':
        cout << "Enemy";
        break;
    case '.':
        cout << "Space";
        break;
    case '-':
        cout << "Light";
        break;
    case '=':
        cout << "Medium";
        break;
    case 'x':
        cout << "Dark";
        break;
    case '#':
        cout << "Block";
        break;
    }
    cout << "\n";
    for (int x = 0; x < TL; x++) {
        for (int y = 0; y < TB; y++) {
            cout << map[x][y];
        }
        cout << endl;
    }
}

void saveDesign(char map[L][B]) {
    fstream outfile;
    remove(mapname);
    outfile.open(mapname, std::ofstream::out | std::ofstream::app);
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < B; j++) {
            outfile << map[i][j];
        }
    }
    outfile.close();
}

void saveTextureSize(int size) {
    fstream outfile;
    remove(texturename);
    outfile.open(texturename, std::ofstream::out | std::ofstream::app);
    outfile << size;
    outfile.close();
}

void saveTexture(char map[TL][TB], char type) {
    fstream outfile;
    outfile.open(texturename, std::ofstream::out | std::ofstream::app);
    outfile << type;
    for (int i = 0; i < TL; i++) {
        for (int j = 0; j < TB; j++) {
            outfile << map[i][j];
        }
    }
    outfile.close();
}

void loadMap(char map[L][B]) {
    ifstream infile;
    infile.open(mapname);
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < B; j++) {
            infile >> map[i][j];
        }
    }
    infile.close();
}

void loadTexture(char map[TL][TB]) {
    ifstream infile;
    infile.open(texturename);
    for (int i = 0; i < TL; i++) {
        for (int j = 0; j < TB; j++) {
            infile >> map[i][j];
        }
    }
    infile.close();
}

void getDesign(char map[L][B]) {
    int i = 1, j = 1;
    char temp = map[i][j];
    map[i][j] = -37;
    bool getting = true;
    while (getting) {
        display(map);
        switch (_getch()) {
        case 'w': case 'W':
            map[i--][j] = temp;
            temp = map[i][j];
            map[i][j] = -37;
            break;
        case 's': case 'S':
            map[i++][j] = temp;
            temp = map[i][j];
            map[i][j] = -37;
            break;
        case 'a': case 'A':
            map[i][j--] = temp;
            temp = map[i][j];
            map[i][j] = -37;
            break;
        case 'd': case 'D':
            map[i][j++] = temp;
            temp = map[i][j];
            map[i][j] = -37;
            break;
        case '*': case '1':
            temp = '*';
            break;
        case 'e': case 'E': case '2':
            temp = 'e';
            break;
        case '.': case '>': case '3':
            temp = '.';
            break;
        case '-': case '_': case '4':
            temp = '-';
            break;
        case '=': case '+': case '5':
            temp = '=';
            break;
        case 'x': case 'X': case '6':
            temp = 'x';
            break;
        case '#': case '7':
            temp = '#';
            break;
        case '\r':
            map[i][j] = temp;
            saveDesign(map);
            getting = !getting;
            break;
        default:
            cout << endl << "Wrong Input";
            _getch();
        }
    }
}

void getTexture(char map[TL][TB]) {
    int i = 1, j = 1;
    char type[7] = { '*', 'e', '.', '-', '=', 'x', '#' };
    saveTextureSize(TL);
    for (int id = 0; id < 7; id++) {
        texturepreset(map);
        char temp = map[i][j];
        map[i][j] = -37;
        bool getting = true;
        while (getting) {
            displayTexture(map, type[id]);
            switch (_getch()) {
            case 'w': case 'W':
                map[i--][j] = temp;
                temp = map[i][j];
                map[i][j] = -37;
                break;
            case 's': case 'S':
                map[i++][j] = temp;
                temp = map[i][j];
                map[i][j] = -37;
                break;
            case 'a': case 'A':
                map[i][j--] = temp;
                temp = map[i][j];
                map[i][j] = -37;
                break;
            case 'd': case 'D':
                map[i][j++] = temp;
                temp = map[i][j];
                map[i][j] = -37;
                break;
            case 'r': case 'R':
                texturepreset(map);
                temp = map[i][j];
                map[i][j] = -37;
            case '1':
                temp = '*'; //Player
                break;
            case '2':
                temp = 'e'; //Enemy (to be implemented)
                break;
            case '3':
                temp = ' ';
                break;
            case '4':
                temp = 250; //Center Dot
                break;
            case '5':
                temp = ':';
                break;
            case '6':
                temp = 176; //Light
                break;
            case '7':
                temp = 177; //Medium
                break;
            case '8':
                temp = 178; //Dark
                break;
            case '9':
                temp = 219; //Full Block
                break;
            case '-': case '_':
                temp = 220; //Top half block
                break;
            case '=': case '+':
                temp = 223; //Bottom half block
                break;

            //Single-Line Borders
            case 't': case 'T':
                temp = 218; //tl
                break;
            case 'y': case 'Y':
                temp = 194; //tm
                break;
            case 'u': case 'U':
                temp = 191; //tr
                break;
            case 'g': case 'G':
                temp = 195; //ml
                break;
            case 'h': case 'H':
                temp = 197; //mm
                break;
            case 'j': case 'J':
                temp = 180; //mr
                break;
            case 'b': case 'B':
                temp = 192; //bl
                break;
            case 'n': case 'N':
                temp = 193; //bm
                break;
            case 'm': case 'M':
                temp = 217; //br
                break;
            case 'f': case 'F':
                temp = 196; //lr
                break;
            case 'v': case 'V':
                temp = 179; //ud
                break;

            //Double-Line Borders
            case 'i': case 'I':
                temp = 201; //tl
                break;
            case 'o': case 'O':
                temp = 203; //tm
                break;
            case 'p': case 'P':
                temp = 187; //tr
                break;
            case 'k': case 'K':
                temp = 204; //ml
                break;
            case 'l': case 'L':
                temp = 206; //mm
                break;
            case ';': case ':':
                temp = 185; //mr
                break;
            case ',': case '<':
                temp = 200; //bl
                break;
            case '.': case '>':
                temp = 200; //bm
                break;
            case '\/': case '?':
                temp = 188; //br
                break;
            case '[': case '{':
                temp = 205; //lr
                break;
            case '\'':case '\"':
                temp = 186; //ud
                break;
            case '\r':
                map[i][j] = temp;
                saveTexture(map, type[id]);
                getting = !getting;
                break;
            default:
                cout << endl << "Wrong Input";
                _getch();
            }
        }
    }
}

int main()
{
    //mapname[20] = 8;
    int option = 0;
    while (option != 6) {
        cout << "1. Design Map\n2. Design Texture\n3. Play Procedurally Generated Maps in 2D\n4. Play in 2D\n5. Play in 3D\n6. Exit\n";
        cin >> option;
        if (option == 1) {
            char map[L][B];
            int option;
            cout << "Load Map or Create Map?\n1. Load\n2. Create\n\n";
            cin >> option;
            if (option == 1)
                loadMap(map);
            if (option == 2)
                preset(map);
            getDesign(map);
        }
        else if (option == 2) {
            char texture[TL][TB];
            int option;
            cout << "Load Map or Create Map?\n1. Load\n2. Create\n\n";
            cin >> option;
            if (option == 1)
                loadTexture(texture);
            if (option == 2)
                texturepreset(texture);
            getTexture(texture);
        }
        else if (option == 3) {
            maximize();
            system("..\\3D_CLI_ASCII\\proceduralgeneration.py");
        }
        else if (option == 4) {
            maximize();
            fstream outfile;
            outfile.open("mapname.txt", std::ofstream::out);
            outfile << mapname << "\n" << texturename;
            outfile.close();
            system("..\\3D_CLI_ASCII\\cpp_redirect_for_2d.py");
            exit(1);
        }
        else if (option == 5) {
            maximize();

            //Screen

            CONSOLE_SCREEN_BUFFER_INFO csbi;
            GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
            int nScreenWidth = csbi.srWindow.Right - csbi.srWindow.Left + 1;
            int nScreenHeight = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;

            wchar_t* screen = new wchar_t[nDisplayWidth * nDisplayHeight];
            HANDLE hConsole = CreateConsoleScreenBuffer(GENERIC_READ | GENERIC_WRITE, 0, NULL, CONSOLE_TEXTMODE_BUFFER, NULL);
            SetConsoleActiveScreenBuffer(hConsole);
            DWORD dwBytesWritten = 0;

            fstream  mapfile;
            mapfile.open(mapname, ios::in);
            string mapBuffer;
            mapfile >> mapBuffer;
            wstring map(mapBuffer.length(), L' ');
            copy(mapBuffer.begin(), mapBuffer.end(), map.begin());

            for (int y = 0; y < nMapHeight; y++) {
                for (int x = 0; x < nMapWidth; x++) {
                    if (map[y * nMapHeight + x] == '*') {
                        fPlayerX = x;
                        fPlayerY = y;
                        map[y * nMapHeight + x] = '.';
                        break;
                    }
                }
            }

            auto tp1 = chrono::system_clock::now();
            auto tp2 = chrono::system_clock::now();

            bool mouse = true;
            bool escape = false;

            for (unsigned int arb = 1; !escape; arb++) {
                GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
                nScreenWidth = csbi.srWindow.Right - csbi.srWindow.Left + 1;
                nScreenHeight = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;

                tp2 = chrono::system_clock::now();
                chrono::duration<float> elapsedTime = tp2 - tp1;
                tp1 = tp2;
                float fElapsedTime = elapsedTime.count();

                //Controls
                GetCursorPos(&p);
                if (arb % 15 == 0 && mouse)
                    SetCursorPos(nDisplayWidth / 2, nDisplayHeight / 2);
                if (GetAsyncKeyState((unsigned short)'M'))
                    mouse = !mouse;
                if (GetAsyncKeyState((unsigned short)'L'))
                    escape = true;
                if ((GetAsyncKeyState((unsigned short)'C') & 0x8000) && fFOV >= fFOVmin) {
                    fFOV = fFOV - 0.03f;
                }
                if ((GetAsyncKeyState((unsigned short)'V') & 0x8000) && fFOV <= fFOVmax) {
                    fFOV = fFOV + 0.03f;
                }
                if (GetAsyncKeyState((unsigned short)'R') & 0x8000) {
                    fFOV = FOV;
                    zAngle = 0.0f;
                }
                if ((mouse && p.x > nDisplayWidth / 2.0) || (GetAsyncKeyState((unsigned short)'D') & 0x8000)) {
                    fPlayerA -= fHorizontalRotation * fElapsedTime;
                    if (fPlayerA < 0)
                        fPlayerA += pi * 2;
                }
                if ((mouse && p.x < nDisplayWidth / 2.0) || (GetAsyncKeyState((unsigned short)'A') & 0x8000)) {
                    fPlayerA += fHorizontalRotation * fElapsedTime;
                    if (fPlayerA > pi * 2)
                        fPlayerA -= pi * 2;
                }
                if ((mouse && p.y < nDisplayHeight / 2.0) || (GetAsyncKeyState(VK_SPACE) & 0x8000)) {
                    zAngle += fVerticalRotation * fElapsedTime;
                }
                if ((mouse && p.y > nDisplayHeight / 2.0) || (GetAsyncKeyState(VK_LSHIFT) & 0x8000)) {
                    zAngle -= fVerticalRotation * fElapsedTime;
                }
                if (GetAsyncKeyState((unsigned short)'W') & 0x8000) {
                    fPlayerX += sinf(fPlayerA) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerX -= sinf(fPlayerA) * 5.0f * fElapsedTime;
                    fPlayerY += cosf(fPlayerA) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerY -= cosf(fPlayerA) * 5.0f * fElapsedTime;
                }
                if (GetAsyncKeyState((unsigned short)'S') & 0x8000) {
                    fPlayerX -= sinf(fPlayerA) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerX += sinf(fPlayerA) * 5.0f * fElapsedTime;
                    fPlayerY -= cosf(fPlayerA) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerY += cosf(fPlayerA) * 5.0f * fElapsedTime;
                }
                if (GetAsyncKeyState((unsigned short)'Q') & 0x8000) {
                    fPlayerX += sinf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerX -= sinf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                    fPlayerY += cosf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerY -= cosf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                }
                if (GetAsyncKeyState((unsigned short)'E') & 0x8000) {
                    fPlayerX -= sinf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerX += sinf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                    fPlayerY -= cosf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                    if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == '#')
                        fPlayerY += cosf(fPlayerA + pi / 2) * 5.0f * fElapsedTime;
                }
                if (map[(int)fPlayerY * nMapWidth + (int)fPlayerX] == 'x') {
                    escape = true;
                }

                for (int x = 0; x < nScreenWidth; x++) {
                    float fRayAngle = (fPlayerA + fFOV / 2.0f) - ((float)x / (float)nScreenWidth) * fFOV;

                    float fDistanceToWall = 0;
                    bool bHitWall = false;
                    bool bHitGate = false;
                    bool bBoundary = false;

                    float fEyeX = sin(fRayAngle);
                    float fEyeY = cos(fRayAngle);

                    while (!bHitWall && !bHitGate && fDistanceToWall < fDepth) {
                        fDistanceToWall += 0.1f;

                        int nTestX = (int)(fPlayerX + fEyeX * fDistanceToWall);
                        int nTestY = (int)(fPlayerY + fEyeY * fDistanceToWall);

                        if (nTestX < 0 || nTestX >= nMapWidth || nTestY < 0 || nTestY >= nMapHeight) {
                            bHitWall = true;
                            fDistanceToWall = fDepth;
                        }
                        else {
                            bHitWall = (map[nTestY * nMapWidth + nTestX] == '#');
                            bHitGate = (map[nTestY * nMapWidth + nTestX] == 'x');
                            if (bHitWall || bHitGate) {

                                vector<pair<float, float>> p;

                                for (int tx = 0; tx < 2; tx++)
                                    for (int ty = 0; ty < 2; ty++) {
                                        float vy = (float)nTestY + ty - fPlayerY;
                                        float vx = (float)nTestX + tx - fPlayerX;
                                        float d = sqrt(vx * vx + vy * vy);
                                        float dot = (fEyeX * vx / d) + (fEyeY * vy / d);
                                        p.push_back(make_pair(d, dot));
                                    }

                                sort(p.begin(), p.end(), [](const pair<float, float>& left, const pair<float, float>& right) {return left.first < right.first; });

                                if (wallCreases) {
                                    float fBound = 0.01;
                                    if (acos(p.at(0).second) < fBound)  bBoundary = true;
                                    if (acos(p.at(1).second) < fBound)  bBoundary = true;
                                }
                            }

                        }
                    }

                    int nCeiling = (float)(nScreenHeight / 2.0) - nScreenHeight / ((float)fDistanceToWall * 2) + zAngle;    //Adjust vertical angle system
                    int nFloor = nScreenHeight - nCeiling + zAngle * 2;

                    short nShade = ' ';
                    short nFloorShade = ' ';

                    if (bHitGate)                                   nShade = ':';
                    else if (fDistanceToWall <= fDepth / 4.0f)      nShade = 0x2588;
                    else if (fDistanceToWall < fDepth / 3.0f)       nShade = 0x2593;
                    else if (fDistanceToWall < fDepth / 2.0f)       nShade = 0x2592;
                    else if (fDistanceToWall < fDepth)              nShade = 0x2591;
                    else                                            nShade = ' ';

                    if (bBoundary) {
                        if (fDistanceToWall < fDepth / 4.0f)        nShade = 0x2593;
                        else if (fDistanceToWall < fDepth / 2.0f)   nShade = 0x2592;
                        else if (fDistanceToWall < fDepth)          nShade = 0x2591;
                    }

                    for (int y = 0; y < nScreenHeight; y++) {
                        if (y < nCeiling)
                            screen[y * nScreenWidth + x] = ' ';
                        else if (y > nCeiling && y < nFloor)
                            screen[y * nScreenWidth + x] = nShade;
                        else {
                            float b = (1.0f - (((float)y - zAngle - nScreenHeight / 2.0f) / ((float)nScreenHeight / 2.0f)));
                            if (b < 0.25)       nFloorShade = '#';
                            else if (b < 0.5)   nFloorShade = 'x';
                            else if (b < 0.75)  nFloorShade = '.';
                            else if (b < 0.9)   nFloorShade = '-';
                            else                nFloorShade = ' ';
                            screen[y * nScreenWidth + x] = nFloorShade;
                        }
                    }

                }



                swprintf_s(screen, 41, L"X=%3.2f, Y=%3.2f, A=%3.2f FPS=%3.2f ", fPlayerX, fPlayerY, fPlayerA * 180.0 / pi, 1.0f / fElapsedTime);

                wstring nPlayerIcon;


                if (fPlayerA * 180.0 / pi > 22.5 && fPlayerA * 180.0 / pi <= 67.5)              nPlayerIcon = L"┌┤┴┘";
                else if (fPlayerA * 180.0 / pi > 67.5 && fPlayerA * 180.0 / pi <= 112.5)        nPlayerIcon = L"┌\\└/";
                else if (fPlayerA * 180.0 / pi > 112.5 && fPlayerA * 180.0 / pi <= 157.5)       nPlayerIcon = L"┬┐└┤";
                else if (fPlayerA * 180.0 / pi > 157.5 && fPlayerA * 180.0 / pi <= 202.5)       nPlayerIcon = L"/\\└┘";
                else if (fPlayerA * 180.0 / pi > 202.5 && fPlayerA * 180.0 / pi <= 247.5)       nPlayerIcon = L"┌┬├┘";
                else if (fPlayerA * 180.0 / pi > 247.5 && fPlayerA * 180.0 / pi <= 292.5)       nPlayerIcon = L"/┐\\┘";
                else if (fPlayerA * 180.0 / pi > 292.5 && fPlayerA * 180.0 / pi <= 337.5)       nPlayerIcon = L"├┐└┴";
                else if (fPlayerA * 180.0 / pi > 337.5 || fPlayerA * 180.0 / pi <= 22.5)        nPlayerIcon = L"┌┐\\/";
                else                                                                            nPlayerIcon = L"/\\\\/";

                if (showMap) {
                    for (int nx = 0; nx < nMapWidth; nx++) {
                        for (int ny = 0; ny < nMapWidth; ny++)
                        {
                            for (int ncx = 0; ncx < 2; ncx++)
                                for (int ncy = 0; ncy < 2; ncy++) {
                                    if (ny == (int)fPlayerY && nx == (int)fPlayerX)
                                        screen[(ny * 2 + 1 + ncy) * nScreenWidth + nx * 2 + ncx] = nPlayerIcon[ncy * 2 + ncx];
                                    else
                                        screen[(ny * 2 + 1 + ncy) * nScreenWidth + nx * 2 + ncx] = map[ny * nMapWidth + nx];
                                }
                        }
                    }
                }


                //Check Actual Screen Width
                //for (int u = 0; u < nScreenWidth; u++) {
                //    screen[u] = (wchar_t)(48 + (u / 100) % 10);
                //    screen[u + nScreenWidth] = (wchar_t)(48 + (u / 10) % 10);
                //    screen[u + 2 * nScreenWidth] = (wchar_t)(48 + u % 10);
                //}

                screen[nScreenWidth * nScreenHeight - 1] = '\0';
                WriteConsoleOutputCharacter(hConsole, screen, nScreenWidth * nScreenHeight, { 0, 0 }, &dwBytesWritten);

            }
            for (int i = 0; i < nDisplayWidth * nDisplayHeight; i++) {
                screen[i] = ' ';
            }
            wstring text;
            text += L"                                                                                                                                                        ";
            text += L"  ,ad8888ba,                                                                                88                    88                                    ";
            text += L" d8\"\'    `\"8b                                                             ,d                88              ,d    \"\"                                    ";
            text += L"d8\'                                                                       88                88              88                                          ";
            text += L"88             ,adPPYba,  8b,dPPYba,   ,adPPYb,d8 8b,dPPYba, ,adPPYYba, MM88MMM 88       88 88 ,adPPYYba, MM88MMM 88  ,adPPYba,  8b,dPPYba,  ,adPPYba,  ";
            text += L"88            a8\"     \"8a 88P\'   `\"8a a8\"    `Y88 88P\'   \"Y8 \"\"     `Y8   88    88       88 88 \"\"     `Y8   88    88 a8\"     \"8a 88P\'   `\"8a I8[    \"\"  ";
            text += L"Y8,           8b       d8 88       88 8b       88 88         ,adPPPPP88   88    88       88 88 ,adPPPPP88   88    88 8b       d8 88       88  `\"Y8ba,   ";
            text += L" Y8a.    .a8P \"8a,   ,a8\" 88       88 \"8a,   ,d88 88         88,    ,88   88,   \"8a,   ,a88 88 88,    ,88   88,   88 \"8a,   ,a8\" 88       88 aa    ]8I  ";
            text += L"  `\"Y8888Y\"\'   `\"YbbdP\"\'  88       88  `\"YbbdP\"Y8 88         `\"8bbdP\"Y8   \"Y888  `\"YbbdP\'Y8 88 `\"8bbdP\"Y8   \"Y888 88  `\"YbbdP\"\'  88       88 `\"YbbdP\"\'  ";
            text += L"                                       aa,    ,88                                                                                                       ";
            text += L"                                        \"Y8bbdP\"                                                                                                        ";
            text += L"                                                                                                                                                        ";
            text += L"8b        d8                        I8,        8        ,8I  ,ad8888ba,   888b      88 88                                                               ";
            text += L" Y8,    ,8P                         `8b       d8b       d8\' d8\"\'    `\"8b  8888b     88 88                                                               ";
            text += L"  Y8,  ,8P                           \"8,     ,8\"8,     ,8\" d8\'        `8b 88 `8b    88 88                                                               ";
            text += L"   \"8aa8\" ,adPPYba,  88       88      Y8     8P Y8     8P  88          88 88  `8b   88 88                                                               ";
            text += L"    `88\' a8\"     \"8a 88       88      `8b   d8\' `8b   d8\'  88          88 88   `8b  88 88                                                               ";
            text += L"     88  8b       d8 88       88       `8a a8\'   `8a a8\'   Y8,        ,8P 88    `8b 88 \\\/                                                               ";
            text += L"     88  \"8a,   ,a8\" \"8a,   ,a88        `8a8\'     `8a8\'     Y8a.    .a8P  88     `8888 db                                                               ";
            text += L"     88   `\"YbbdP\"\'   `\"YbbdP\'Y8         `8\'       `8\'       `\"Y8888Y\"\'   88      `888 9P                                                               ";
            for (int tx = 0; tx < 152; tx++)
                for (int ty = 0; ty < 20; ty++)
                    screen[ty * nScreenWidth + tx] = text[ty * 152 + tx];
            for (int i = 0; i < 500; i++)
                WriteConsoleOutputCharacter(hConsole, screen, nScreenWidth * nScreenHeight, { 0, 0 }, &dwBytesWritten);
            exit(1);
        }
        else if (option == 4) {
            system("cls");
            cout << "Thank you for using our Game Engine.";
            _getch();
        }
    }
    return 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started:
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
