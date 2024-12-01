import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.6.10" // Kotlin Plugin, adjust version as needed
    id("java")
    id("application")
    id("com.github.johnrengelman.shadow") version "7.0.0" // For creating a fat JAR
}

group = "com.syphercore"
version = "1.0-SNAPSHOT"
application {
    mainClass.set("com.syphercore.MainKt") // Adjust main class accordingly
}

repositories {
    mavenCentral() // The central Maven repository for dependency management
    jcenter() // Additional repository, optional
}

dependencies {
    implementation(kotlin("stdlib"))
    
    // Hedera SDK dependency
    implementation("com.hedera.hashgraph:sdk:2.10.0") // Replace with a suitable version
    
    // Ring Signatures - BouncyCastle for cryptographic features
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")
    implementation("org.bouncycastle:bcpkix-jdk15on:1.70")

    // zk-SNARKs dependencies, for example:
    implementation("com.zokrates:zokrates-core:0.7.11") // Replace with relevant zk-SNARK tooling

    // Jackson for JSON parsing (if required for zk-SNARK proofs, etc.)
    implementation("com.fasterxml.jackson.core:jackson-databind:2.12.5")

    // Logging
    implementation("ch.qos.logback:logback-classic:1.2.7")

    // Testing
    testImplementation("org.junit.jupiter:junit-jupiter:5.8.1")
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        jvmTarget = "11" // Set to the JVM version compatible with your environment
    }
}

tasks.test {
    useJUnitPlatform()
}

// Optional shadowJar task to create a fat JAR for deployment
tasks {
    val shadowJar by getting(com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar::class) {
        archiveClassifier.set("")
        manifest {
            attributes(mapOf("Main-Class" to "com.syphercore.MainKt")) // Set the correct main class
        }
    }
}
