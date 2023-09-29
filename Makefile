##
## EPITECH PROJECT, 2023
## Makefile
## File description:
## Makefile
##

CC		:=		gcc
NAME	:=		libgoogcrypto.so
SRC		:=		googcrypto/hasher.c		\
				googcrypto/googcrypto.c
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
	rm -rf $(OBJ)

fclean:	clean
	rm -rf $(NAME)

re:	fclean	all

# valgrind: all
#	valgrind $(VFLAGS) ./$(NAME)

.SILENT:

.PHONY:	all	clean	fclean	re