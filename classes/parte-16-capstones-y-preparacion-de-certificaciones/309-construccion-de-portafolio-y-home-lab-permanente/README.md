# Clase 309 — Construcción de portafolio y home lab permanente

> Parte: **16 — Capstones y preparación de certificaciones** · Fuente: *The Cyber Plumber's Handbook · DetectionLab · buenas prácticas de la comunidad*
> ⏱️ Duración estimada: **120 min** · Nivel: **Intermedio**

---

## 🎯 Objetivo

Convertir el trabajo de las 308 clases anteriores en **evidencia empleable**: un portafolio público (writeups, informes anonimizados, repos) y un **home lab permanente y reproducible** donde seguir practicando. El objetivo es que un reclutador o cliente pueda, en cinco minutos, verificar tu competencia real. Integra los entregables de los capstones (Clases 303, 305, 306, 307, 308) en una vitrina profesional.

> ⚠️ **Ética**: al publicar, **anonimiza** cualquier dato de sistemas reales o de programas de bug bounty (respeta sus políticas de divulgación). Nunca publiques credenciales, PII ni detalles fuera de scope. Usa solo laboratorios propios o datos ficticios.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Estructurar** un portafolio con proyectos, writeups e informes.
2. **Publicar** contenido técnico anonimizado y bien presentado.
3. **Desplegar** un home lab reproducible con infraestructura como código.
4. **Documentar** el laboratorio para que otros (y tu yo futuro) lo reconstruyan.
5. **Presentar** su perfil profesional coherente (GitHub, blog, LinkedIn).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Qué incluir en el portafolio | Evidencia, no listas de temas |
| 2 | Writeups y CTFs | Demuestran razonamiento, no solo resultado |
| 3 | Informes anonimizados | Muestran redacción profesional |
| 4 | Home lab con IaC | Reproducible y versionado |
| 5 | Blog técnico y GitHub | Presencia pública verificable |
| 6 | Anonimización y ética | Publicar sin exponer datos |
| 7 | Marca profesional | Coherencia entre plataformas |

## 📖 Definiciones y características

- **Portafolio**: colección curada de trabajo demostrable. *Característica*: prioriza calidad y evidencia sobre cantidad.
- **Writeup**: explicación paso a paso de cómo resolviste un reto. *Característica*: revela tu proceso de pensamiento.
- **Infraestructura como código (IaC)**: definir el lab en archivos (Vagrant/Terraform/Ansible). *Característica*: reproducible y versionable.
- **Home lab**: entorno personal de práctica permanente. *Característica*: aislado, seguro y desechable.
- **Anonimización**: eliminar datos identificables antes de publicar. *Característica*: obligatoria en informes reales.
- **Marca profesional**: coherencia de perfil entre GitHub, blog y LinkedIn. *Característica*: facilita que te encuentren.

## 🧰 Herramientas y preparación

- **GitHub/GitLab** para repos y para alojar el blog (GitHub Pages).
- Blog estático: **Hugo**, **Jekyll** o **MkDocs**.
- Home lab IaC: **Vagrant** + **VirtualBox**/**Proxmox**, **Ansible** para aprovisionar, o plantillas tipo **DetectionLab**.
- Los entregables de los capstones (Clases 303–308) como base del portafolio.
- Una plantilla de writeup y una de informe anonimizado.

## 🧪 Laboratorio guiado

1. **Inventaria tu trabajo.** Lista los entregables de los capstones (informe pentest 303, Red Team 305, Blue Team 306, DFIR 307, reporte 308) y selecciona los mejores.
2. **Anonimiza.** Reemplaza IPs, nombres y datos reales por valores ficticios; verifica que no queda PII.
3. **Crea el repo del portafolio.** Estructura: `/writeups`, `/informes`, `/homelab`, `/tools`, con un `README.md` índice.
4. **Escribe 2 writeups.** Elige dos máquinas/retos y documenta el razonamiento (no solo la solución).
5. **Monta el blog.** Genera un sitio con MkDocs/Hugo y publica los writeups; despliega en GitHub Pages.
6. **Codifica el home lab.** Escribe un `Vagrantfile` que levante tu laboratorio base (Kali + víctima + SIEM):

   ```ruby
   Vagrant.configure("2") do |config|
     config.vm.define "kali" do |k|
       k.vm.box = "kalilinux/rolling"
       k.vm.network "private_network", ip: "10.10.10.5"
     end
   end
   ```

7. **Aprovisiona con Ansible.** Automatiza la instalación de herramientas para reconstruir el lab en minutos.
8. **Documenta el lab.** Un `README` con diagrama de red, cómo levantarlo (`vagrant up`) y cómo destruirlo.
9. **Unifica tu marca.** Enlaza GitHub ↔ blog ↔ LinkedIn con la misma identidad y descripción.

## ✍️ Ejercicios

1. Estructura el árbol de carpetas de tu portafolio.
2. Anonimiza un informe de capstone y verifica que no queda dato real.
3. Escribe un writeup completo de una máquina.
4. Crea un `Vagrantfile` que levante dos VMs en una red privada.
5. Publica el blog en GitHub Pages con al menos un post.
6. Redacta un README de home lab reproducible con diagrama.

## 📝 Reto verificable

Publica un **portafolio** (repo público + blog) que incluya: índice, al menos 2 writeups, 1 informe de capstone anonimizado y un **home lab como código** (Vagrant/Ansible) con documentación para levantarlo.

**Criterio de aceptación**: un tercero puede clonar el repo y levantar el home lab con un comando documentado, el blog es accesible públicamente, los informes no contienen datos reales, y el índice enlaza todos los artefactos.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| "Publiqué datos reales" | Anonimización incompleta; revisa IPs, hostnames y capturas antes de subir. |
| "Nadie entiende mis writeups" | Falta contexto; explica el razonamiento, no solo comandos. |
| "El lab no se reproduce" | Pasos manuales sin IaC; automatiza con Vagrant/Ansible. |
| "El blog no despliega" | Config de Pages incorrecta; revisa rama y ruta de publicación. |
| "Mi perfil está disperso" | Sin marca coherente; unifica identidad entre plataformas. |

## ❓ Preguntas frecuentes

**❓ ¿GitHub privado o público?**
Público para el portafolio (es la vitrina). Mantén privado lo sensible o inacabado.

**❓ ¿Cuántos writeups necesito?**
Pocos y buenos superan a muchos mediocres. Empieza con 2–3 que muestren razonamiento.

**❓ ¿Puedo publicar informes de bug bounty?**
Solo si el programa lo permite y tras la divulgación coordinada. Anonimiza siempre.

**❓ ¿Vale usar la nube en vez de local?**
Sí, pero cuida costes y aislamiento. Un lab local con Vagrant es gratuito y controlado.

## 🔗 Referencias

- DetectionLab: <https://github.com/clong/DetectionLab>
- Vagrant: <https://www.vagrantup.com/> · Ansible: <https://docs.ansible.com/>
- MkDocs: <https://www.mkdocs.org/> · GitHub Pages: <https://pages.github.com/>
- GOAD (lab AD): <https://github.com/Orange-Cyberdefense/GOAD>
- OWASP Vulnerable Web Applications Directory: <https://owasp.org/www-project-vulnerable-web-applications-directory/>

## ➡️ Siguiente clase

[Clase 310 - Plan de aprendizaje continuo y comunidad](../310-plan-de-aprendizaje-continuo-y-comunidad/README.md)
