<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Tymon\JWTAuth\Facades\JWTAuth;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    // =========================================================================
    // POST /api/register
    // =========================================================================

    public function test_register_successfully(): void
    {
        $response = $this->postJson('/api/register', [
            'name'                  => 'Test User',
            'email'                 => 'test@example.com',
            'password'              => 'password123',
            'password_confirmation' => 'password123',
        ]);

        $response->assertStatus(201)
                 ->assertJsonStructure(['message', 'user' => ['id', 'name', 'email']]);
    }

    public function test_register_fails_duplicate_email(): void
    {
        User::factory()->create(['email' => 'test@example.com']);

        $response = $this->postJson('/api/register', [
            'name'                  => 'Test User',
            'email'                 => 'test@example.com',
            'password'              => 'password123',
            'password_confirmation' => 'password123',
        ]);

        $response->assertStatus(422);
    }

    public function test_register_fails_password_too_short(): void
    {
        $response = $this->postJson('/api/register', [
            'name'                  => 'Test User',
            'email'                 => 'short@example.com',
            'password'              => '123',
            'password_confirmation' => '123',
        ]);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['password']);
    }

    public function test_register_fails_password_mismatch(): void
    {
        $response = $this->postJson('/api/register', [
            'name'                  => 'Test User',
            'email'                 => 'mismatch@example.com',
            'password'              => 'password123',
            'password_confirmation' => 'different456',
        ]);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['password_confirmation']);
    }

    public function test_register_fails_missing_name(): void
    {
        $response = $this->postJson('/api/register', [
            'email'                 => 'noname@example.com',
            'password'              => 'password123',
            'password_confirmation' => 'password123',
        ]);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['name']);
    }

    public function test_register_fails_invalid_email_format(): void
    {
        $response = $this->postJson('/api/register', [
            'name'                  => 'Test User',
            'email'                 => 'not-an-email',
            'password'              => 'password123',
            'password_confirmation' => 'password123',
        ]);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['email']);
    }

    // =========================================================================
    // POST /api/login
    // =========================================================================

    public function test_login_successfully(): void
    {
        User::factory()->create([
            'email'    => 'test@example.com',
            'password' => Hash::make('password123'),
        ]);

        $response = $this->postJson('/api/login', [
            'email'    => 'test@example.com',
            'password' => 'password123',
        ]);

        $response->assertStatus(200)
                 ->assertJsonStructure(['access_token', 'token_type', 'expires_in']);
    }

    public function test_login_returns_bearer_token_type(): void
    {
        User::factory()->create([
            'email'    => 'bearer@example.com',
            'password' => Hash::make('password123'),
        ]);

        $response = $this->postJson('/api/login', [
            'email'    => 'bearer@example.com',
            'password' => 'password123',
        ]);

        $response->assertStatus(200)
                 ->assertJsonPath('token_type', 'bearer');
    }

    public function test_login_fails_wrong_password(): void
    {
        User::factory()->create([
            'email'    => 'test@example.com',
            'password' => Hash::make('password123'),
        ]);

        $response = $this->postJson('/api/login', [
            'email'    => 'test@example.com',
            'password' => 'wrong-password',
        ]);

        $response->assertStatus(401)
                 ->assertJson(['message' => 'Credenciales inválidas']);
    }

    public function test_login_fails_wrong_credentials(): void
    {
        $response = $this->postJson('/api/login', [
            'email'    => 'noexiste@example.com',
            'password' => 'wrongpassword',
        ]);

        $response->assertStatus(401);
    }

    public function test_login_fails_missing_fields(): void
    {
        $response = $this->postJson('/api/login', []);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['email', 'password']);
    }

    // =========================================================================
    // Rutas protegidas (JWT)
    // =========================================================================

    public function test_protected_route_without_token(): void
    {
        $response = $this->getJson('/api/me');
        $response->assertStatus(401);
    }

    public function test_me_returns_authenticated_user(): void
    {
        $user = User::factory()->create([
            'email'    => 'me@example.com',
            'password' => Hash::make('password123'),
        ]);

        $token = JWTAuth::fromUser($user);

        $response = $this->withHeader('Authorization', "Bearer $token")
                         ->getJson('/api/me');

        $response->assertStatus(200)
                 ->assertJsonPath('email', 'me@example.com');
    }

    public function test_me_fails_with_invalid_token(): void
    {
        $response = $this->withHeader('Authorization', 'Bearer token_invalido')
                         ->getJson('/api/me');

        $response->assertStatus(401);
    }

    public function test_logout_successfully(): void
    {
        $user  = User::factory()->create([
            'password' => Hash::make('password123'),
        ]);
        $token = JWTAuth::fromUser($user);

        $response = $this->withHeader('Authorization', "Bearer $token")
                         ->postJson('/api/logout');

        $response->assertStatus(200)
                 ->assertJson(['message' => 'Sesión cerrada exitosamente']);
    }

    // =========================================================================
    // POST /api/forgot-password
    // =========================================================================

    public function test_forgot_password_invalid_email(): void
    {
        $response = $this->postJson('/api/forgot-password', ['email' => 'notvalid']);
        $response->assertStatus(422);
    }

    public function test_forgot_password_missing_email(): void
    {
        $response = $this->postJson('/api/forgot-password', []);
        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['email']);
    }

    public function test_forgot_password_valid_email_returns_200(): void
    {
        \Illuminate\Support\Facades\Notification::fake();
        \Illuminate\Auth\Notifications\ResetPassword::createUrlUsing(
            fn($user, $token) => "http://localhost/reset-password?token={$token}"
        );

        User::factory()->create(['email' => 'valid@example.com']);

        $response = $this->postJson('/api/forgot-password', [
            'email' => 'valid@example.com',
        ]);

        $response->assertStatus(200);
    }
}