/*
 * Reto 1 — Desbordamiento de búfer en el stack (material de laboratorio).
 * DELIBERADAMENTE VULNERABLE. Solo para práctica local en el contenedor aislado.
 *
 * Objetivo didáctico: `gets()` no limita la entrada, así que se puede desbordar
 * `buffer` y sobrescribir la dirección de retorno. La función `secreto()` no se
 * llama nunca desde main: el reto es desviar el flujo hasta ella.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void secreto(void) {
    puts("[+] Has redirigido el flujo a secreto(). Reto resuelto.");
    system("/bin/sh");
}

void vulnerable(void) {
    char buffer[64];
    puts("Introduce tu nombre:");
    gets(buffer);            /* <- vulnerabilidad: sin límite de longitud */
    printf("Hola, %s\n", buffer);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    vulnerable();
    puts("Fin normal del programa.");
    return 0;
}
