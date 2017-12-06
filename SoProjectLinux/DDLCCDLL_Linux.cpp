//---------------------------------------
// DDLCCDLL.cpp (The Doki Doki Literature Club C Dynamic Link Library)
// This contains (as of 2017-11-25) all the more low-level functionality.
// This includes things like interfacing with the recycle bin.
// To build the DLL and copy it to the Renpy project, set the build config on Release, and build the solution.
// (In VS Community, this should be the top bar, next to the undo/redo buttons)
// To test functionality outside of the Renpy project, set the config to Debug.
// This will also generate a debug console application, which is based off of main().
// I don't know for sure, but it's probably best to use x86 (32-bit) for actual compilation.
//---------------------------------------

//#include <Windows.h>
//#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <cstring>
//TODO : this file seems linux only, find out how to do this for mac.
#include <fts.h>
//#include <Python.h>

#define UNICODE

#if defined(_UNICODE) || defined(UNICODE)
typedef wchar_t TCHAR;
typedef wchar_t* PTSTR;
#define StrCmp(x,y) wcscmp(x,y)
#else
typedef char TCHAR;
typedef char* PTSTR;
#define StrCmp(x,y) strcmp(x,y)
#endif

using namespace std;

struct LocalFileInfo
{
public:
    LocalFileInfo():fileName(nullptr),filePath(nullptr),fileSize(-1){}
    LocalFileInfo(const LocalFileInfo& other):fileName(other.fileName),filePath(other.filePath),fileSize(other.fileSize){}
    LocalFileInfo(TCHAR* f, TCHAR* p, int s):fileName(f), filePath(p), fileSize(s){}
    TCHAR* fileName;
    TCHAR* filePath;
    int fileSize;
};

//Marks a function that needs to be exported to the DLL, if you want something in the Renpy project, this is how you do it.
#define EXPORT(type) extern "C" {\
/*/__declspec(dllexport)*/ type /*__cdecl*/

//For consistency, you end with this define, although you could technically just use a curly bracket as well.
#define END }


//Internal vectors and maps, these will be used instead of actually accessing the Recycle bin directly.
vector<PTSTR> recycleBinFiles;
map<PTSTR, LocalFileInfo> recycleBinEntries;

// Ensures that the files in our internal vector are up to date. Preferrably called each time you try accessing the bin
EXPORT(void) UpdateFilesInRecycleBin()
{
    //Clean up previous loop
    for (auto it = recycleBinEntries.begin(); it != recycleBinEntries.end(); ++it)
    {
        delete[] it->second.fileName;
        delete[] it->second.filePath;
    }
    recycleBinEntries.clear();
    recycleBinFiles.clear();

    FTS* ftsp;
    char path[260];
    memset(path,0,260);
    strcpy(path, getenv("HOME"));
    strcat(path, "/.local/share/Trash/files");
    //For mac, the path seems to be UserFolder/.Trash

    int fts_options = FTS_COMFOLLOW | FTS_LOGICAL | FTS_NOCHDIR;

    char* paths[2];
    paths[0] = path;
    paths[1] = nullptr;

    ftsp = fts_open(paths, fts_options, nullptr);

    if(ftsp == nullptr)
    {
        cout << "Error fetching files from recycle bin\n";
        return;
    }

    FTSENT* chp = fts_children(ftsp, 0);
    if (chp == NULL)
    {
        return;               /* no files to traverse */
    }
    FTSENT* p = nullptr;
    while ((p = fts_read(ftsp)) != nullptr)
    {
        switch (p->fts_info)
        {
            case FTS_D:
                cout << "Found subdirectory " << p->fts_path << "\n";
                break;
            case FTS_F:
            {

                cout << "Found file " << p->fts_name << "\n";
                size_t length = p->fts_namelen+1;
                wchar_t* convertedName = new wchar_t[length];
                wchar_t* convertedPath = new wchar_t[p->fts_pathlen+1];
                mbstowcs(convertedName, p->fts_name, length);
                mbstowcs(convertedPath, p->fts_path, p->fts_pathlen+1);

                ifstream fileStr(p->fts_path, ifstream::ate | ifstream::binary);
                int size = (int) fileStr.tellg();

                recycleBinFiles.push_back(convertedName);
                recycleBinEntries[convertedName] = LocalFileInfo(convertedName, convertedPath, size);
                break;
            }//
            case FTS_DC:
                cout << "Found cycle directory " << p->fts_path << "\n";
                break;
            case FTS_DEFAULT:
                cout << "Found default thing " << p->fts_path << "\n";
                break;
            case FTS_DNR:
                cout << "Found unreadable dir " << p->fts_path << "\n";
                break;
            case FTS_DOT:
                cout << "Found dot file " << p->fts_path << "\n";
                break;
            case FTS_DP:
                cout << "Found post order dir " << p->fts_path << "\n";
                break;
            case FTS_ERR:
                cout << "Jesus take the wheel we found an error\n";
                break;
            case FTS_NS:
                cout << "no stat info with error\n";
                break;
            case FTS_NSOK:
                cout << "no stat info\n";
                break;
            case FTS_SL:
                cout << "symbolic link\n";
                break;
            case FTS_SLNONE:
                cout << "symbolic link no target\n";
                break;
            default:
                cout << "Found something I don't know about\n";
                break;
          }
    }
    fts_close(ftsp);

    return;
}
END

// Pretty much what it says on the tin.
EXPORT(int) GetRecycleBinFileCount()
{
	//Culls the size disparity warning. I don't think anyone will ever have more than 2147483647 files in their recycle bin.
	return (int)recycleBinFiles.size();
}
END

// Technically the way you should get the files, but Python seems to have issues with pointers to pointers.
// Returns an array of c-strings containing the files currently in the recycle bin
EXPORT(PTSTR*) GetRecycleBinFiles()
{
	return recycleBinFiles.data();
}
END

// Get the Recycle bin filename string in the internal vector using the index.
EXPORT(PTSTR) GetRecycleBinFileAt(int i)
{
	return recycleBinFiles[i];
}
END

//Gets the Item ID for a filename. Internal only.
LocalFileInfo* GetFile(const TCHAR* fileName)
{
    for (auto it = recycleBinEntries.begin(); it != recycleBinEntries.end() ; ++it)
	{
		if (StrCmp(fileName, it->first) == 0)
		{
			return & it->second;
		}
	}

	return nullptr;
}

// Checks if the given file exists in the recycle bin (extension only)
EXPORT(bool) BinContainsFile(const TCHAR* fileName)
{
	wcout << "[RecycleBin] Asked for "<<fileName << "\n";
	return GetFile(fileName) != nullptr;
}
END

//Gets the size of a file in the recycle bin
EXPORT(int) GetRBFileSize(const TCHAR* fileName)
{
    LocalFileInfo* info = GetFile(fileName);
    if(info == nullptr)
	   return -1;
    return info->fileSize;
}
END

//Checks if a files size matches the given size.
EXPORT(bool) VerifySize(const TCHAR* fileName, int size)
{
	int real = GetRBFileSize(fileName);

	//Files should have a size.
	if (real < 0) return false;

	return real == size;
}
END

//Helper vector for RedeleteFile
vector<PTSTR> pathsToRemove;

//// [TODO] NOT IMPLEMENTED : Requires both Restore and RedeleteFile to work
////Checks if a file matches the given checksum. Uses the CRC32 checksum to verify if the file is matching.
//EXPORT(bool) VerifyChecksumCRC32(const TCHAR* fileName, int crcCompare)
//{
//	LPITEMIDLIST pidl = GetFile(fileName);
//
//	if (pidl == nullptr)
//	{
//		return false;
//	}
//
//	PTSTR str = GetFilePath(pRecycleBin, pidl);
//
//	RestoreFile(pidl,str);
//
//	RedeleteFile(str);
//
//	UpdateFilesInRecycleBin();
//
//	return false;
//}
//END

//---------------------------------------------
// DEBUG MAIN FUNCTION (Ran when in debug mode)
//---------------------------------------------
int main()
{
	UpdateFilesInRecycleBin();

    //cout << ;

	for (auto i = recycleBinFiles.begin(); i != recycleBinFiles.end(); ++i)
	{
		//wcout << i->first << "\n";
		wcout << "Size of " << *i << " = " << GetRBFileSize(*i) << "\n";
	}

	//RedeleteFile(TEXT("C:\\Users\\Andreas\\Downloads\\RecycleBin_src\\ReadMe.txt"));

	//if (VerifyChecksumCRC32(TEXT("Hello.txt"), 0x4d170e0e))
	//{
	//	cout << "Yes\n";
	//}
	//else
	//{
	//	cout << "No\n";
	//}

    return 0;
}
