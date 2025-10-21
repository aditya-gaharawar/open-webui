<!-- 
  Email Verification Page Example for OpenWebUI/AnswerAI
  Place this in: src/routes/auth/verify/+page.svelte
-->

<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  let status: 'pending' | 'success' | 'error' = 'pending';
  let message = 'Verifying your email...';
  let token = '';

  onMount(async () => {
    // Get token from URL query parameters
    token = $page.url.searchParams.get('token') || '';

    if (!token) {
      status = 'error';
      message = 'Invalid verification link. Please check your email for the correct link.';
      return;
    }

    try {
      const response = await fetch('/api/v1/email-verification/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      });

      const data = await response.json();

      if (response.ok) {
        status = 'success';
        message = data.message || 'Email verified successfully!';
        
        // Redirect to login page after 3 seconds
        setTimeout(() => {
          goto('/auth');
        }, 3000);
      } else {
        status = 'error';
        message = data.detail || 'Verification failed. Please try again.';
      }
    } catch (error) {
      status = 'error';
      message = 'An error occurred during verification. Please try again.';
      console.error('Verification error:', error);
    }
  });

  async function resendEmail() {
    // You might want to get the email from somewhere or ask the user
    const email = prompt('Please enter your email address:');
    
    if (!email) return;

    try {
      const response = await fetch('/api/v1/email-verification/resend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message || 'Verification email has been sent!');
      } else {
        alert(data.detail || 'Failed to resend verification email');
      }
    } catch (error) {
      alert('An error occurred. Please try again.');
      console.error('Resend error:', error);
    }
  }
</script>

<svelte:head>
  <title>Email Verification - AnswerAI</title>
</svelte:head>

<div class="verification-container">
  <div class="verification-card">
    {#if status === 'pending'}
      <div class="icon-container">
        <div class="spinner"></div>
      </div>
      <h1>Verifying Email</h1>
      <p>{message}</p>
    {:else if status === 'success'}
      <div class="icon-container success">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="2"
          stroke="currentColor"
          class="check-icon"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h1 class="success-title">Email Verified!</h1>
      <p>{message}</p>
      <p class="redirect-message">Redirecting to login page...</p>
      <a href="/auth" class="btn-primary">Go to Login Now</a>
    {:else if status === 'error'}
      <div class="icon-container error">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="2"
          stroke="currentColor"
          class="error-icon"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <h1 class="error-title">Verification Failed</h1>
      <p>{message}</p>
      <div class="action-buttons">
        <button on:click={resendEmail} class="btn-secondary">
          Resend Verification Email
        </button>
        <a href="/auth" class="btn-primary">Back to Login</a>
      </div>
    {/if}
  </div>
</div>

<style>
  .verification-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
  }

  .verification-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    padding: 48px;
    max-width: 500px;
    width: 100%;
    text-align: center;
    animation: slideUp 0.5s ease-out;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .icon-container {
    width: 80px;
    height: 80px;
    margin: 0 auto 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #f3f4f6;
  }

  .icon-container.success {
    background: #d1fae5;
    color: #059669;
  }

  .icon-container.error {
    background: #fee2e2;
    color: #dc2626;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e5e7eb;
    border-top-color: #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .check-icon,
  .error-icon {
    width: 48px;
    height: 48px;
  }

  h1 {
    font-size: 28px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 16px;
  }

  .success-title {
    color: #059669;
  }

  .error-title {
    color: #dc2626;
  }

  p {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 12px;
    line-height: 1.5;
  }

  .redirect-message {
    font-size: 14px;
    color: #9ca3af;
    margin-top: 24px;
    margin-bottom: 16px;
  }

  .action-buttons {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 24px;
  }

  .btn-primary,
  .btn-secondary {
    display: inline-block;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    cursor: pointer;
    border: none;
    font-size: 16px;
    width: 100%;
  }

  .btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
  }

  .btn-secondary {
    background: #f3f4f6;
    color: #374151;
  }

  .btn-secondary:hover {
    background: #e5e7eb;
  }

  @media (max-width: 640px) {
    .verification-card {
      padding: 32px 24px;
    }

    h1 {
      font-size: 24px;
    }

    p {
      font-size: 14px;
    }
  }
</style>
