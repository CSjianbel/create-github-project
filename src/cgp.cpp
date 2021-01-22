#include <iostream>

int main(int argc, char *argv[])
{
    if (argc != 3 || argc != 4)
    {
        std::cout << "Usage: ./gcp [author] [repository name] [license*]" << std::endl;
        return 1;
    }

    std::string author = argv[1];
    std::string repoName = argv[2];
    std::string license(argc == 4 ? argv[3] : "MIT");

}
