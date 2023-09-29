##
## EPITECH PROJECT, 2023
## Makefile
## File description:
## Makefile
##

CC		:=		gcc
ifeq ($(OS),Windows_NT)
NAME	:=		lib\\libgoogcrypto.dll
SRC		:=		googcrypto\\hasher.c		\
				googcrypto\\googcrypto.c
else
NAME	:=		lib/libgoogcrypto.dll
SRC		:=		googcrypto/hasher.c		\
				googcrypto/googcrypto.c
endif
# PROD
CFLAGS	:=		-O3 -fPIC -shared
# DEBUG
DFLAGS	:=		-Wall -Wextra -Werror -ansi -pedantic -fPIC -shared
OBJ		:=		$(SRC:.c=.o)
VFLAGS	:=		--track-origins=yes --show-leak-kinds=all	\
				--leak-check=full -s --trace-children=yes	\
				--read-inline-info=yes --read-var-info=yes	\
				--errors-for-leak-kinds=all

all:	$(NAME)

$(NAME):	$(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

clean:
ifeq ($(OS),Windows_NT)
	erase /q /f $(OBJ)
else
	rm -rf $(OBJ)
endif

fclean:	clean
ifeq ($(OS),Windows_NT)
	erase /q /f $(NAME)
else
	rm -rf $(NAME)
endif

re:	fclean	all

# valgrind: all
#	valgrind $(VFLAGS) ./$(NAME)

.SILENT:

.PHONY:	all	clean	fclean	re