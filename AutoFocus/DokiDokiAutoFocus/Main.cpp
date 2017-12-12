///-------------------------------------------
/// DOKI DOKI AUTO FOCUS
///
/// This is a program that inputs a file, and automatically applies focus transforms to whichever Doki is currently talking.
/// It saves a couple of minutes of painstakingly typing it manually. Do check if it's good though afterwards
/// Hardcoded to do Doki Doki stuff.
///-------------------------------------------

#include <cstring>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

enum class Doki
{
	Null,
	Sayori,
	Yuri,
	Monika,
	Natsuki,
};


Doki currentDoki = Doki::Null;
int sayoriTransformNum;
int yuriTransformNum;
int monikaTransformNum;
int natsukiTransformNum;

bool CheckHopFocus(wofstream& stream, Doki checkDoki, wchar_t* buffer, int at_start, int whitespace, int& transformNum);
bool CheckTransform(wchar_t* buffer, int start, int max, int& transformNum, Doki checkDoki, wofstream& stream, int whitespace);
void EvalDoki(wofstream& stream, Doki newDoki, int whiteSpace);

bool CheckHopFocus(wofstream& stream, Doki checkDoki, wchar_t* buffer, int at_start, int whitespace, int& transformNum)
{
	if (currentDoki != checkDoki)
	{
		EvalDoki(stream, checkDoki, whitespace);
		//return false;
	}

	wchar_t* newBuff = new wchar_t[wcslen(buffer) + 2];

	wmemcpy(newBuff, buffer, at_start);
	wmemcpy(newBuff + at_start, L"at hf", 5);
	wcscpy(newBuff + at_start + 5, buffer + at_start + 4);

	stream << newBuff << L'\n';

	at_start += 4;
	if (buffer[at_start] >= '0' && buffer[at_start] <= '9' && buffer[at_start + 1] >= '0' && buffer[at_start + 1] <= '9')
	{
		transformNum = (buffer[at_start] - '0') * 10 + (buffer[at_start + 1] - '0');
	}

	delete[] newBuff;

	return true;
}

bool CheckTransform(wchar_t* buffer, int start, int max, int& transformNum, Doki checkDoki, wofstream& stream, int whitespace)
{
	for (int j = start; j < max-start; j++)
	{
		//Check the transform number
		if (wmemcmp(buffer + j, L"at t",4) == 0)
		{
			//the next part will be the transform
			j += 4;
			if (buffer[j] >= '0' && buffer[j] <= '9' && buffer[j + 1] >= '0' && buffer[j + 1] <= '9')
			{
				transformNum = (buffer[j] - '0') * 10 + (buffer[j + 1] - '0');
			}
			break;
		}
		//Check if it's a hop transform
		else if (wmemcmp(buffer + j, L"at h", 4) == 0)
		{
			return CheckHopFocus(stream, checkDoki, buffer, j, whitespace, transformNum);
		}
		if (buffer[j] == 0) break;
	}
	return false;
}

void EvalDoki(wofstream& stream, Doki newDoki, int whiteSpace)
{
	//If we have the same doki, return
	if (currentDoki == newDoki)
	{
		return;
	}

	//Preserve whitespace
	if (currentDoki != Doki::Null)
	{
		for (int i = 0; i < whiteSpace; i++)
		{
			stream << ' ';
		}
	}

	//Reset the previous doki's transform
	switch (currentDoki)
	{
		case Doki::Null:
			break;
		case Doki::Sayori:
			stream << L"show sayori at t" << sayoriTransformNum << L'\n';
			break;
		case Doki::Yuri:
			stream << L"show yuri at t" << yuriTransformNum << L'\n';
			break;
		case Doki::Monika:
			stream << L"show monika at t" << monikaTransformNum << L'\n';
			break;
		case Doki::Natsuki:
			stream << L"show natsuki at t" << natsukiTransformNum << L'\n';
			break;
		default:
			break;
	}

	//Set the new doki's transform, if we confirmed a transform
	switch (newDoki)
	{
		case Doki::Null:
			break;
		case Doki::Sayori:
			if (sayoriTransformNum <= 0) return;
			for (int i = 0; i < whiteSpace; i++)
			{
				stream << ' ';
			}
			stream << L"show sayori at f" << sayoriTransformNum << L'\n';
			break;
		case Doki::Yuri:
			if (yuriTransformNum <= 0) return;
			for (int i = 0; i < whiteSpace; i++)
			{
				stream << ' ';
			}
			stream << L"show yuri at f" << yuriTransformNum << L'\n';
			break;
		case Doki::Monika:
			if (monikaTransformNum <= 0) return;
			for (int i = 0; i < whiteSpace; i++)
			{
				stream << ' ';
			}
			stream << L"show monika at f" << monikaTransformNum << L'\n';
			break;
		case Doki::Natsuki:
			if (natsukiTransformNum <= 0) return;
			for (int i = 0; i < whiteSpace; i++)
			{
				stream << ' ';
			}
			stream << L"show natsuki at f" << natsukiTransformNum << L'\n';
			break;
		default:
			break;
	}
	currentDoki = newDoki;
}

int main(int argc, char* argv[])
{
	if (argc < 2) return -1;

	char* newFileName = nullptr;
	if (argc > 2)
	{
		//Copy the output path. Has to be full path
		int len =(int) strlen(argv[2]) + 1;
		newFileName = new char[len];

		strcpy(newFileName, argv[2]);
		newFileName[len - 1] = 0;
	}
	else
	{
		//Get a name based on the old file.
		int len =(int) strlen(argv[1]) + 1 + 4;
		newFileName = new char[len];

		memset(newFileName, 0, len);
		strcpy(newFileName, argv[1]);
		strcpy(newFileName + strlen(argv[1]), "_out");
	}

	//Open both the input and output stream at the same time.
	wifstream input( argv[1], ios::in );
	wofstream output(newFileName, ios::out | ios::trunc);

	int prevSpaceCount = -1;

	//Iterate over each line of the file
	while (input.good())
	{
		wchar_t buffer[9000];
		memset(buffer, 0, 9000);
		input.getline(buffer, 9000);

		int curSpaceCount = 0;
		bool foundData = false;
		bool writeLine = true;

		for (int i = 0; i < 9000; i++)
		{
			//Check for whitespace
			if (!foundData && buffer[i] == L' ')
			{
				++curSpaceCount;
			}
			else if (!foundData)
			{
				foundData = true;

				//If the indentation is different from previous line, make sure to reset
				if (curSpaceCount != prevSpaceCount)
				{
					EvalDoki(output, Doki::Null, prevSpaceCount);
				}
				prevSpaceCount = curSpaceCount;
				//Check which char is speaking based on the prefix.
				if (buffer[i] == L's' && buffer[i+1] == L' ')
				{
					EvalDoki(output, Doki::Sayori, curSpaceCount);
				}
				else if (buffer[i] == L'y' && buffer[i+1] == L' ')
				{
					EvalDoki(output, Doki::Yuri, curSpaceCount);
				}
				else if (buffer[i] == L'm' && buffer[i+1] == L' ')
				{
					EvalDoki(output, Doki::Monika, curSpaceCount);
				}
				else if (buffer[i] == L'n' && buffer[i+1] == L' ')
				{
					EvalDoki(output, Doki::Natsuki, curSpaceCount);
				}
				else if (buffer[i] == L'"')
				{
					EvalDoki(output, Doki::Null, curSpaceCount);
				}
				//DDLC RB specific character 
				else if (wmemcmp(buffer + i, L"sim ", 4) == 0)
				{
					EvalDoki(output, Doki::Null, curSpaceCount);
				}
				//Check if we're doing a show command, which could change the transform, or just the emotion.
				else if (wmemcmp(buffer + i, L"show ", 5) == 0)
				{
					i += 5;

					//Verify the character.
					if (wmemcmp(buffer + i, L"sayori", 6) == 0)
					{
						//this sets current doki transform num probably
						i += 7;
						writeLine = !CheckTransform(buffer, i, 9000, sayoriTransformNum, Doki::Sayori, output,curSpaceCount);
						break;
					}
					else if (wmemcmp(buffer + i, L"yuri", 4) == 0)
					{
						i += 5;
						writeLine = !CheckTransform(buffer, i, 9000, yuriTransformNum,Doki::Yuri, output,curSpaceCount);
						break;
					}
					else if (wmemcmp(buffer + i, L"monika", 6) == 0)
					{
						i += 7;
						writeLine = !CheckTransform(buffer, i, 9000, monikaTransformNum,Doki::Monika, output,curSpaceCount);
					}
					else if (wmemcmp(buffer + i, L"natsuki", 7) == 0)
					{
						i += 8;
						writeLine = !CheckTransform(buffer, i, 9000, natsukiTransformNum,Doki::Natsuki, output,curSpaceCount);
						break;
					}
				}
				//Check if we're hiding a character, which means we need to reset the transform.
				else if (wmemcmp(buffer + i, L"hide ", 5) == 0)
				{
					i += 5;

					if (wmemcmp(buffer + i, L"sayori", 6) == 0)
					{
						sayoriTransformNum = 0;
						if(currentDoki == Doki::Sayori)
						{
							currentDoki = Doki::Null;
						}
					}
					else if (wmemcmp(buffer + i, L"yuri", 4) == 0)
					{
						yuriTransformNum = 0;
						if(currentDoki == Doki::Yuri)
						{
							currentDoki = Doki::Null;
						}
					}
					else if (wmemcmp(buffer + i, L"monika", 6) == 0)
					{
						monikaTransformNum = 0;
						if(currentDoki == Doki::Monika)
						{
							currentDoki = Doki::Null;
						}
					}
					else if (wmemcmp(buffer + i, L"natsuki", 7) == 0)
					{
						natsukiTransformNum = 0;
						if(currentDoki == Doki::Natsuki)
						{
							currentDoki = Doki::Null;
						}
					}
					break;
				}
				//Cancel out if statements
				else if (wmemcmp(buffer + i, L"if", 2) == 0 || wmemcmp(buffer + i, L"else", 4) == 0 || wmemcmp(buffer + i, L"elif", 4) == 0)
				{
					EvalDoki(output, Doki::Null, prevSpaceCount);
				}
			}
			if (buffer[i] == 0)
			{
				break;
			}

		}
		if(writeLine)
			output << buffer << L'\n';
	}
	input.close();
	output.close();

	
	delete[] newFileName;
	
}