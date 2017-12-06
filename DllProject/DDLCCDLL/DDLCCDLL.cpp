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
#include <tchar.h>
#include <ShlObj.h>
#include <shlwapi.h>
//#include <fstream>
#include <propkey.h>
#include <vector>
#include <map>
#include <cstring>
//#include <Python.h>

using namespace std;

//Marks a function that needs to be exported to the DLL, if you want something in the Renpy project, this is how you do it.
#define EXPORT(type) extern "C" {\
__declspec(dllexport) type __cdecl 

//For consistency, you end with this define, although you could technically just use a curly bracket as well.
#define END }

//Gets the original file path of the recycle bin file (using its itemid)
PTSTR GetFilePath(IShellFolder *psf, PCUITEMID_CHILD pidl)
{
	STRRET sr;
	PTSTR out;
	HRESULT hr = psf->GetDisplayNameOf(pidl, SHGDN_NORMAL, &sr);
	if (SUCCEEDED(hr)) {
		hr = StrRetToStr(&sr, pidl, &out);
		//if (SUCCEEDED(hr)) {
		//	_tprintf(TEXT("%s = %s\n"), pszLabel, pszName);
		//
		//
		return out;
	}
	return nullptr;
}

//Gets the name of a recycle bin file (using its itemid)
PTSTR GetFileName(IShellFolder *psf, PCUITEMID_CHILD pidl)
{
	STRRET sr;
	PTSTR out;
	HRESULT hr = psf->GetDisplayNameOf(pidl, SHGDN_INFOLDER, &sr);
	if (SUCCEEDED(hr)) {
		hr = StrRetToStr(&sr, pidl, &out);
		//if (SUCCEEDED(hr)) {
		//	_tprintf(TEXT("%s = %s\n"), pszLabel, pszName);
		//
		//
		return out;
	}
	return nullptr;
}

LPSHELLFOLDER pDesktop = NULL;
LPITEMIDLIST pidlRecycleBin = NULL;
IShellFolder2 *pRecycleBin = NULL;
LPENUMIDLIST pEnumFiles;

//Internal vectors and maps, these will be used instead of actually accessing the Recycle bin directly.
vector<PTSTR> recycleBinFiles;
map<PTSTR, LPITEMIDLIST> recycleBinEntries;

// Ensures that the files in our internal vector are up to date. Preferrably called each time you try accessing the bin
EXPORT(void) UpdateFilesInRecycleBin()
{
	//Initialize the vars needed if necessary
	if (pDesktop == NULL)
	{
		SHGetDesktopFolder(&pDesktop);
		SHGetSpecialFolderLocation(NULL, CSIDL_BITBUCKET, &pidlRecycleBin);
		pDesktop->BindToObject(pidlRecycleBin, NULL, IID_IShellFolder2, (LPVOID *)&pRecycleBin);
	}
	for (auto it = recycleBinEntries.begin(); it != recycleBinEntries.end(); it++)
	{
		//Code references cotaskmemfree in the context of freeing strings, so I do that here.
		CoTaskMemFree(it->first);
		CoTaskMemFree(it->second);
	}
	recycleBinFiles.clear();
	recycleBinEntries.clear();

	pRecycleBin->EnumObjects(NULL, /*SHCONTF_FOLDERS|*/SHCONTF_NONFOLDERS|SHCONTF_INCLUDEHIDDEN,
							 &pEnumFiles);
	
	LPITEMIDLIST pidl = NULL;

	while (pEnumFiles->Next(1, &pidl, NULL) != S_FALSE)
	{
		PTSTR str = GetFileName(pRecycleBin, pidl);
		if (str != nullptr)
		{
			recycleBinFiles.push_back(str);
		}

		wcout << "[RecycleBin] Found " << str << "\n";

		recycleBinEntries.insert_or_assign(str, pidl);
	}
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
LPITEMIDLIST GetFile(const TCHAR* fileName)
{
	for (auto it = recycleBinEntries.begin(); it != recycleBinEntries.end() ; ++it)
	{
		if (StrCmp(fileName, it->first) == 0)
		{
			return it->second;
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
	if (pRecycleBin == nullptr)
	{
		return -1;
	}

	LPITEMIDLIST pidl = GetFile(fileName);
	if (pidl == nullptr)
	{
		return -1;
	}

	VARIANT vt;
	HRESULT hr = pRecycleBin->GetDetailsEx(pidl, &PKEY_Size, &vt);
	if (SUCCEEDED(hr)) {
		hr = VariantChangeType(&vt, &vt, 0, VT_INT);
		if (SUCCEEDED(hr)) {
			return V_INT(&vt);
		}
		VariantClear(&vt);
	}
	return -1;
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

//Helper function for RestoreFile
void InvokeVerb(IContextMenu *pcm, PCSTR pszVerb)
{
	HMENU hmenu = CreatePopupMenu();
	if (hmenu) {
		HRESULT hr = pcm->QueryContextMenu(hmenu, 0, 1, 0x7FFF, CMF_NORMAL);
		if(SUCCEEDED(hr)) {
			CMINVOKECOMMANDINFO info = { 0 };
			info.cbSize = sizeof(info);
			info.lpVerb = pszVerb;
			pcm->InvokeCommand(&info);
		}
		DestroyMenu(hmenu);
	}
}

//Copied from that CodeProjects thing, may have been too old.
//Helper function for RestoreFile
BOOL ExecCommand (LPITEMIDLIST pidl, LPCSTR lpszCommand)
{
	BOOL bReturn = FALSE;
	LPCONTEXTMENU pCtxMenu = NULL;
	HRESULT hr = S_OK;

	hr = pRecycleBin->GetUIObjectOf (nullptr, 1, (LPCITEMIDLIST *)&pidl, IID_IContextMenu, NULL, (LPVOID *)&pCtxMenu);
	
	if (SUCCEEDED (hr))
	{
		InvokeVerb(pCtxMenu, lpszCommand);
	}

	pCtxMenu->Release();

	return bReturn;
}

//Helper function for RestoreFile
HRESULT GetUIObjectOfFile(HWND hwnd, LPCWSTR pszPath, REFIID riid, void **ppv)
{
	*ppv = NULL;
	HRESULT hr;
	LPITEMIDLIST pidl;
	SFGAOF sfgao;
	if (SUCCEEDED(hr = SHParseDisplayName(pszPath, NULL, &pidl, 0, &sfgao))) {
		IShellFolder *psf;
		LPCITEMIDLIST pidlChild;
		if (SUCCEEDED(hr = SHBindToParent(pidl, IID_IShellFolder,
			(void**)&psf, &pidlChild))) {
			hr = psf->GetUIObjectOf(hwnd, 1, &pidlChild, riid, NULL, ppv);
			psf->Release();
		}
		CoTaskMemFree(pidl);
	}
	return hr;
}

//Helper function for RestoreFile
void DropOnRestoreFolder(IDataObject *pdto, PTSTR totalPath)
{
	int strLen = lstrlen(totalPath);
	PTSTR str2 = new TCHAR[strLen + 1];
	bool foundFirstSlash = false;
	for (int i = strLen; i >= 0; --i)
	{
		if (!foundFirstSlash)
		{
			str2[i] = '\0';
		}
		else
		{
			str2[i] = totalPath[i];
		}

		if (totalPath[i] == '\\')
		{
			foundFirstSlash = true;
		}
	}

	IDropTarget *pdt;
	if (SUCCEEDED(GetUIObjectOfFile(NULL,
		str2,
		IID_PPV_ARGS(&pdt)))) {
		POINTL pt = { 0, 0 };
		DWORD dwEffect = DROPEFFECT_MOVE;
		if (SUCCEEDED(pdt->DragEnter(pdto, MK_LBUTTON,
			pt, &dwEffect))) {
			dwEffect &= DROPEFFECT_MOVE;
			if (dwEffect) {
				pdt->Drop(pdto, MK_LBUTTON, pt, &dwEffect);
			} else {
				pdt->DragLeave();
			}
		}
		pdt->Release();
	}

	delete[] str2;
}

// [TODO] NOT IMPLEMENTED : Restores a file in the recycle bin to its former path. Somehow this doesn't seem to work, despite the code being near-identical... Needs investigation.
void RestoreFile(LPITEMIDLIST pidl, PTSTR fullPath)
{
	//Check the directory path, see which paths exist, and add the ones to the list that we have to hard delete.
	//ExecCommand(pidl, "undelete");

	IDataObject* pDataObj = NULL;
	HRESULT hr = S_OK;

	hr = pRecycleBin->GetUIObjectOf (nullptr, 1, (LPCITEMIDLIST *)&pidl, IID_IDataObject, NULL, (LPVOID *)&pDataObj);
	if (SUCCEEDED(hr)) {
		DropOnRestoreFolder(pDataObj,fullPath);
		pDataObj->Release();
	}
}

// PARTIALLY IMPLEMENTED : Puts a file in the recycle bin. Is actually meant to be used to put a file in the recycle bin that was previously restored, and should also clean up any mess left behind.
void RedeleteFile(PTSTR str)
{
	//Put the file back into the recycle bin, also delete all folders that were created whilst restoring the file.
	//IFileOperation::DeleteItem()

	wcout << str << "\n";
	cout << str << "\n";

	PZZTSTR str2 = new TCHAR[lstrlen(str) + 2];

	int strLen = lstrlen(str);

	cout << "StrLen : " << strLen << " - Sizeof : " << sizeof(TCHAR) << "\n";

	memcpy(str2, str, strLen * sizeof(TCHAR));
	//This needs to be double null terminated. It's annoying, but oh well.
	str2[strLen] = '\0';
	str2[strLen+1] = '\0';

	SHFILEOPSTRUCT op = {0};
	op.wFunc = FO_DELETE;
	op.pFrom = str2;
	op.fFlags = FOF_ALLOWUNDO | FOF_NO_UI;
	
	int x = SHFileOperation(&op);
	if (x != 0)
	{
		cout << "WOAH THERE PAL\n";
	}

	delete[] str2;
}

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
	for (auto i = recycleBinFiles.begin(); i != recycleBinFiles.end(); ++i)
	{
		//wcout << i->first << "\n";
		wcout << "Size of " << *i << " = " << GetRBFileSize(*i) << "\n";
	}

	if (BinContainsFile(TEXT("Hello.txt")))
	{
		cout << "Hello from the other siiiiiiiiiiiiiiiiiide\n";
	}
	else
	{
		cout << "You say goodbye and I say JSDAKLGJDIOFUE\n";
		return 0;
	}
	
	if (VerifySize(TEXT("Hello.txt"), 2))
	{
		cout << "It fits, I sits\n";
	}
	else
	{
		wcout << L"It's too big senpai \nうぐう\n";
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
