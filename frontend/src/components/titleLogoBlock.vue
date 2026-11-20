<template>
  <div class="title-logo-block">
    <div class="logo"></div>
    <div class="title">Signy</div>
  </div>
</template>
<style scoped>
.title-logo-block {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  .logo {
    max-width: 43px;
    max-height: 35px;
    height: 28px;
    width: 34px;
    mask-image: url("@/assets/icons/logo.png");
    mask-size: cover;
    background-color: var(--color-lightpink);
  }
  .title {
    color: var(--color-purple);
    font-family: var(--font-family);
    font-size: var(--font-size-title);
  }
}
</style>
