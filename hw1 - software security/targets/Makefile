# tools
CC := gcc
RM := rm -f
CP := cp

# flags
CFLAGS := -ggdb -g3
LDFLAGS :=
LDLIBS :=

# sources
sources := target0.c target1.c target2.c target3.c target5.c
targets := target0 target1 target2 target3 target4 target5

# gmake magic
.PHONY: default all clean

#targets
default: all target4
all: $(targets)

target4: target4.c
	gcc -ggdb -g3 target4.c tmalloc.c -o target4


install: $(targets)
	-$(RM) /tmp/target?
	$(CP) $(targets) /tmp


setuid:
ifeq ($(shell id -u),0)
	chown root:root /tmp/target?
	chmod 4755 /tmp/target?
else
	@echo "'make setuid' must be run as root -- use su or a root login!"
endif


clean:
	$(RM) $(targets) $(sources:.c=.o)
